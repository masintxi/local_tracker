from math import sqrt, isclose

ABSOLUTE_TOLERANCE = 1e-6

class Receiver():
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
        self.is_active = False

class Tracker():
    def __init__(self, id, x = 0, y = 0):
        # Initialize the tracker at an impossible (physical) position 
        # that could be inside a wall or outside the building (0, 0)
        self.id = id
        self.__x = x
        self.__y = y
        self.is_active = False

    def report(self, receiver):
        # This function will return the relative distance between
        # the current tracker and the pointed receiver
        return self.__measure_distance(self.__x, self.__y, receiver.x, receiver.y)
    
    def move_to(self, new_x, new_y):
        # Simulate tracker moving to another position
        self.__x = new_x
        self.__y = new_y

    def find_position(self, receivers):
        if len(receivers) < 2:
            raise ValueError("Not enough trackers.")

        # Report to all the receivers and put the measures on a list
        loc = []
        for rec_id, rec in receivers.items():
            dist = self.report(rec)
            loc.append((dist, rec.x, rec.y, rec_id))

        # Sort the measures by distance and take the 3 lowest
        loc = sorted(loc, key=lambda x: x[0])

        r0, x0, y0, id0 = loc[0] # nearest receiver
        r1, x1, y1, id1 = loc[1] # second nearest receiver

        # Distance between the two first receivers
        dist = sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2)

        # First we check the edge case
        if dist > (r0 + r1 + ABSOLUTE_TOLERANCE):
            # The circles do not intersects, it means something is very wrong
            raise ValueError("Out of range or something is very wrong")
        
        # Usually the circles should intesect in two points and one of them
        # must be our target. Let's calculate this intersection points
        (x3_1, y3_1), (x3_2, y3_2) = self.__calculate_candidate_points(r0, x0, y0, r1, x1, y1, dist)
        # print(f"{self.id} is at: ({round(x3_1, 2)},{round(y3_1, 2)}) or ({round(x3_2, 2)},{round(y3_2, 2)})")

        # If the two candidates are the same point it means the two circles are tangent 
        # and we can calculate the position with two receivers
        if self.__compare_eq_dist(x3_1, x3_2) and self.__compare_eq_dist(y3_1, y3_2):
            # print("Tangency!!!!!!!")
            self.__x , self.__y = x3_1, y3_1
            return (self.__x , self.__y, (id0, id1))

        if len(receivers) < 3:
            err_string = "\n".join([
                    "Position not aquired. Another receiver is needed to resolve",
                    "wich one of the two intersection points is the right one.",
                    f"Could be ({round(x3_1, 2)},{round(y3_1, 2)}) or ({round(x3_2, 2)},{round(y3_2, 2)})"
                    ])
            raise ValueError(err_string, ((x3_1, x3_2), (y3_1, y3_2), (id0, id1)))

        r2, x2, y2, id2 = loc[2] # third nearest receiver

        # Measure the distance from the 3rd receiver to the 2 candidates
        test_p1 = self.__measure_distance(x3_1, y3_1, x2, y2)
        test_p2 = self.__measure_distance(x3_2, y3_2, x2, y2)

        # If the two values returned are the same we test with the other 
        # receivers until we find one that gets two different readings
        if self.__compare_eq_dist(test_p1, test_p2):
            for i in range(3, len(loc)):
                # print(f"{id2} reported equal distance {round(test_p1, 2)}. Using other receiver: {loc[i][3]}")
                r2, x2, y2, id2 = loc[i]
                test_p1 = self.__measure_distance(x3_1, y3_1, x2, y2)
                test_p2 = self.__measure_distance(x3_2, y3_2, x2, y2)
                if not self.__compare_eq_dist(test_p1, test_p2):
                    break
            else:
                err_string = "\n".join([
                    f"Position not aquired. The last receiver ({id2}) can't resolve",
                    "when the two intersection points are at the same distance.",
                    "Recommendation: Reposition the receivers or add more.",
                    f"Could be ({round(x3_1, 2)},{round(y3_1, 2)}) or ({round(x3_2, 2)},{round(y3_2, 2)})"
                    ])
                raise ValueError(err_string, ((x3_1, x3_2), (y3_1, y3_2), (id0, id1, id2)))
        
        # The one that matches the 3rd receiver measure is our taget
        if self.__compare_eq_dist(r2, test_p1):
            self.__x , self.__y = x3_1, y3_1
        elif self.__compare_eq_dist(r2, test_p2):
            self.__x , self.__y = x3_2, y3_2
        else:
            raise ValueError("Could not get position.")
        return (self.__x , self.__y, (id0, id1, id2))

    def __calculate_candidate_points(self, r0, x0, y0, r1, x1, y1, dist):
        # This helper calculates the two points of intersection of 2 circles
        # https://paulbourke.net/geometry/circlesphere/
        # l1 = (r0^2 - r1^2 + dist ^2) / (2*dist)
        l1 = (r0 ** 2 - r1 ** 2 + dist ** 2) / (2 * dist)

        # l2 = sqrt(r0^2 - l1^2)
        l2 = sqrt(abs(r0 ** 2 - l1 ** 2))

        # p2 = p0 + l1 * (p1 - p0) / dist
        x2 = x0 + l1 * (x1 - x0) / dist
        y2 = y0 + l1 * (y1 - y0) / dist

        # This are the two points candidates, the intersection of the 2 circles:
        # x3_1 = x2 + l2 * (y1 - y0) / dist  ||  y3_1 = y2 - l2 * (x1 - x0) / dist
        # x3_2 = x2 - l2 * (y1 - y0) / dist  ||  y3_2 = y2 + l2 * (x1 - x0) / dist 
        return (
            (x2 + l2 * (y1 - y0) / dist, y2 - l2 * (x1 - x0) / dist),
            (x2 - l2 * (y1 - y0) / dist, y2 + l2 * (x1 - x0) / dist)
        )

    def __measure_distance(self, x, y, rx, ry):
        # This helper measures the distance between a given point (x,y)
        # and the given receiver position (rx, ry) 
        dist_x = x - rx
        dist_y = y - ry
        dist = sqrt(dist_x ** 2 + dist_y ** 2)

        return dist

    def __compare_eq_dist(self, d1, d2):
        return isclose(d1, d2, abs_tol=ABSOLUTE_TOLERANCE)



