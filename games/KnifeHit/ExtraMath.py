import numpy as np

import math

def normalizeVector(v):
    mag = math.sqrt(v[0] * v[0] + v[1] * v[1])
    return (v[0] / mag, v[1] / mag)

def getAngleBetweenVectors(v1, v2):
    # Calculate dot product
    dot_product = v1[0] * v2[0] + v1[1] * v2[1]
    
    # Calculate magnitudes
    magnitude_v1 = math.sqrt(v1[0]**2 + v1[1]**2)
    magnitude_v2 = math.sqrt(v2[0]**2 + v2[1]**2)
    
    # Check for zero vectors
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0
    
    # Calculate cosine of angle
    cos_theta = dot_product / (magnitude_v1 * magnitude_v2)
    
    # Clip to valid range [-1, 1] to handle floating point errors
    cos_theta = max(-1.0, min(1.0, cos_theta))
    
    # Calculate angle using arccos and convert to degrees
    angle = math.degrees(math.acos(cos_theta))
    
    return angle

def GetClockwiseAngle(frm, to):
    # Normalize vectors
    frm_norm = frm / np.linalg.norm(frm)
    if np.linalg.norm(to) != 0:
        to_norm = to / np.linalg.norm(to)
    else:
        to_norm = [0, 1]
    
    # Calculate angle using dot product
    cos_angle = np.dot(frm_norm, to_norm)
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    angle_rad = np.arccos(cos_angle)
    angle_deg = np.degrees(angle_rad)
    
    # Determine direction (clockwise vs counterclockwise)
    determinant = frm_norm[0]*to_norm[1] - frm_norm[1]*to_norm[0]
    return angle_deg if determinant > 0 else 360 - angle_deg

def vectorDotProduct(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def angleToVector(angleDeg):
    # Convert angle to radians
    angleRad = math.radians(angleDeg)
    
    # Calculate normalized vector components
    x = math.cos(angleRad)
    y = math.sin(angleRad)
    
    return np.array([x, y])

def rotateVector(v, angleDeg):
    # Convert angle to radians
    angleRad = math.radians(angleDeg)
    
    # Create rotation matrix
    cos_angle = math.cos(angleRad)
    sin_angle = math.sin(angleRad)
    rotation_matrix = np.array([[cos_angle, -sin_angle],[sin_angle, cos_angle]])
    
    # Apply rotation
    rotated_vector = np.dot(rotation_matrix, v)
    
    return rotated_vector