import numpy as np
class BodyDirection:
    def __init__(self, right_shoulder_idx=2, left_shoulder_idx=5, right_hip_idx=8, left_hip_idx=11) -> None:
        self.right_shoulder_idx = right_shoulder_idx
        self.left_shoulder_idx = left_shoulder_idx
        self.right_hip_idx = right_hip_idx
        self.left_hip_idx = left_hip_idx
    def distance(self, point_a, point_b):
        """Calculate distance between 2 points
        Args:
            point_a (float): Point A
            point_b (float): Point B
        Returns:
            float: distance between A and B
        """
        return np.sqrt((point_a[0] - point_b[0])**2 + (point_a[1] - point_b[1]) ** 2)    
    def get_bodysize_value(self, pose, v_ratio=1.5):
        """Body size value
        Args:
            pose (arr): Numpy pose
            v_ratio (float, optional): Body size ratio. Defaults to 1.2.
        Returns:
            float: Max value of body size
        """
        left_shoulder = pose[self.left_shoulder_idx]
        right_shoulder = pose[self.right_shoulder_idx]
        left_hip = pose[self.left_hip_idx]
        right_hip = pose[self.right_hip_idx]
        dist1 = self.distance(left_shoulder, right_shoulder) * v_ratio
        dist2 = self.distance(left_hip, right_hip) * v_ratio
        dist3 = self.distance(left_shoulder, left_hip)
        dist4 = self.distance(right_shoulder, right_hip)
        max_dist = max([dist1, dist2, dist3, dist4])
        return max_dist if max_dist >= 1 else 1  
    def get_direction(self, pose):
        """
        Estimate body direction from pose keypoints 
        Arguments:
            pose: numpy array: [1,17,3]
        Returns:
            return angle counterclockwise
        """
        left_shoulder = pose[self.left_shoulder_idx]
        right_shoulder = pose[self.right_shoulder_idx]
        x_left = left_shoulder[0]
        x_right = right_shoulder[0]
        y_left = left_shoulder[1]
        y_right = right_shoulder[1]
        x_dist = abs(left_shoulder[0] - right_shoulder[0])
        bd_size = self.get_bodysize_value(pose, v_ratio=1.5) * 0.7
        ratio = x_dist/bd_size
        ratio = ratio if ratio <= 1  else 1
        a = np.degrees(np.arccos(ratio))
        if x_right < x_left:
            if y_right > y_left:
                a += 0
            else:
                a = 270 + (90 - a)
        else:
            if y_right > y_left:
                a = 90 + (90 - a)
            else:
                a += 180
        return a

def predict_direction(pose):
    pose = np.array(pose)
    bd_direct = BodyDirection()
    angle = bd_direct.get_direction(pose)
    side_angle = 45
    if 90 - side_angle < angle < side_angle + side_angle or  270 - side_angle < angle < 270 + side_angle:
        direction = "side"
    elif  angle <= 90 - side_angle  or angle >= 270 + side_angle:
        direction = "front"
    else:
        direction = "rear"
    return direction

if __name__== "__main__":
    pose = [[738, 166], 
            [728, 196],
            [693, 196],
            [673, 265],
            [668, 315],
            [762, 196],
            [767, 262],
            [771, 307],
            [688, 298],
            [687, 386],
            [681, 431],
            [755, 298],
            [730, 387],
            [711, 435],
            [724, 247]]
    pose = np.array(pose)
    bd_direct = BodyDirection()
    angle = bd_direct.get_bodysize_value(pose)
    side_angle = 45
    if 90 - side_angle < angle < side_angle + side_angle or  270 - side_angle < angle < 270 + side_angle:
        direction = "side"
    elif  angle <= 90 - side_angle  or angle >= 270 + side_angle:
        direction = "front"
    else:
        direction = "rear"
    print(direction)