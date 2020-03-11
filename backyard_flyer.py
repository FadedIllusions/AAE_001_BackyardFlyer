# Import Necessary Packages
import time
from enum import Enum

import numpy as np

from udacidrone import Drone
from udacidrone.connection import MavlinkConnection, WebSocketConnection  # noqa: F401
from udacidrone.messaging import MsgID



# Define States
class States(Enum):
    MANUAL = 0
    ARMING = 1
    TAKEOFF = 2
    WAYPOINT = 3
    LANDING = 4
    DISARMING = 5



class BackyardFlyer(Drone):


    def __init__(self, connection):
        """ Init Connection, Set Default Target Pos, Def Init State, Register Callbacks """
        super().__init__(connection)
        self.target_position = np.array([0.0, 0.0, 0.0])
        self.all_waypoints = []
        self.in_mission = True
        self.check_state = {}

        # Define Initial State
        self.flight_state = States.MANUAL

        # Register Needed Callbacks
        self.register_callback(MsgID.LOCAL_POSITION, self.local_position_callback)
        self.register_callback(MsgID.LOCAL_VELOCITY, self.velocity_callback)
        self.register_callback(MsgID.STATE, self.state_callback)


    def local_position_callback(self):
        """ Triggers When 'MsgID.LOCAL_POSITION' Received && 'self.local_position' Contains New Data."""

        # If In Takeoff State
        if self.flight_state == States.TAKEOFF:
            # Coordinate Conversion
            # Check If Altitude Within 95% Of Target Altitude
            # Set Waypoints And Begin Transition
            if -1.0*self.local_position[2]>0.95*self.target_position[2]:
                self.all_waypoints = self.calculate_box()
                self.waypoint_transition()
        
        # If Traversing To Waypoint
        elif self.flight_state == States.WAYPOINT:
            # Calculate Vector Norm
            if np.linalg.norm(self.target_position[0:2] - self.local_position[0:2])<1.0:
                # Check If Waypoints Remaining In Queue
                if len(self.all_waypoints)>0:
                    # Transition To Next Waypoint
                    self.waypoint_transition()
                # If Not Any Waypoints In Queue
                # And Able To Land, Transition To Landing State
                else:
                    if np.linalg.norm(self.local_velocity[0:2])<1.0:
                        self.landing_transition()


    def velocity_callback(self):
        """Triggers When `MsgID.LOCAL_VELOCITY` Received && 'self.local_velocity' Contains New Data."""

        # Check If In Landing State
        # Confirm Altitude And Transition To Disarmed State
        if self.flight_state == States.LANDING:
            if self.global_position[2]-self.global_home[2]<0.1:
                if abs(self.local_position[2])<0.01:
                    self.disarming_transition()


    def state_callback(self):
        """Triggers When `MsgID.STATE` Received && 'self.armed' And 'self.guided' Contain New Data."""

        # If In Mission, Iterate Through Transitional States
        if self.in_mission:
            if self.flight_state == States.MANUAL:
                self.arming_transition()
            elif self.flight_state == States.ARMING:
                # Confirm Armed State
                if self.armed:
                    self.takeoff_transition()
            elif self.flight_state == States.DISARMING:
                # Confirm Disarmed State
                if ~self.armed & ~self.guided:
                    self.manual_transition()


    def calculate_box(self):
        """Return Waypoints For Box"""

        # Define Waypoint Distances (Meters) And Home
        print("Setting Home Coordinates")
        local_waypoints = [
                            [15.0, 0.0, 10.0],
                            [15.0, 15.0, 10.0],
                            [0.0, 15.0, 10.0],
                            [0.0, 0.0, 10.0],
                            [-15.0, 0.0, 10.0],
                            [-15.0, -5.0, 10.0],
                            [0.0, -15.0, 10.0],
                            [0.0, 0.0, 10.0]
                          ]

        return local_waypoints


    def arming_transition(self):
        """Enter AutoPilot Mode, Arm Drone, Set Home Location To Current Position, Set Flight State To Arming"""
        
        print("Arming Transition...")

        self.take_control()
        self.arm()
        self.set_home_position(self.global_position[0], self.global_position[1], self.global_position[2])
        self.flight_state = States.ARMING


    def takeoff_transition(self):
        """Set Target Altitude 3 Meters, Command Takeoff To Target Altitude, Transition To TAKEOFF State"""
        
        print("Takeoff Transition...")

        target_altitude = 3.0
        self.target_position[2] = target_altitude
        self.takeoff(target_altitude)
        self.flight_state = States.TAKEOFF


    def waypoint_transition(self):
        """Command Next Waypoint Position, Transition To WAYPOINT State"""
    
        print("Waypoint Transition...")

        self.target_position = self.all_waypoints.pop(0)
        print("Target Position: ", self.target_position)

        self.cmd_position(
                            self.target_position[0],
                            self.target_position[1],
                            self.target_position[2],
                            0.0
                         )
        
        self.flight_state = States.WAYPOINT


    def landing_transition(self):
        """Command Landing, Transition To LANDING State"""
        
        print("Landing Transition...")

        self.land()
        self.flight_state = States.LANDING


    def disarming_transition(self):
        """Command Drone To Disarm, Transition To DISARMING State"""
        
        print("Disarm Transition...")

        self.disarm()
        self.release_control()
        self.flight_state = States.DISARMING


    def manual_transition(self):
        """Release Control, Stop Connection (And Telemetry Log), End Mission, Transition To MANUAL State"""
        
        print("Manual Transition...")

        self.release_control()
        self.stop()
        self.in_mission = False
        self.flight_state = States.MANUAL

    def start(self):
        """Open Log File, Start Connection, Close Log File"""
        
        print("Creating Log File...")
        self.start_log("Logs", "NavLog.txt")

        print("Starting Connection...")
        self.connection.start()

        print("Closing Log File...")
        self.stop_log()


if __name__ == "__main__":
    
    # Init MavlinkConnection Object On TCP Port 5760 Of Local Host
    conn = MavlinkConnection('tcp:127.0.0.1:5760', threaded=False, PX4=False)

    # Init BackyardFlyer Object With Mavlink Connection -- Drone
    drone = BackyardFlyer(conn)

    # Delay 2 Seconds
    time.sleep(2)
    
    # Init Drone Start Sequence
    drone.start()
