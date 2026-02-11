#!/usr/bin/env python # 
"""
Author: Thibault ABILY
Date: 18/01/2026 
Contact : thibault.abily@gmail.com
Status: in development
Description: This script will gives all the mechanical torsor associated to mechanical connections defined in a model

Mechanical joints naming convention

French name        | English keyword (code)
--------------------------------------------
Pivot              -> revolute
Glissière          -> prismatic
Rotule             -> spherical
Encastrement       -> fixed
Appui ponctuel     -> fixed_point
"""

import numpy as np

class Joint :
    """
    Mechanical joint defined at a point.
    """

    # Available joint types (class-level)
    JOINT_TYPES = {
        "revolute": {
            "french": "Pivot",
            "axis_required": True,
            "description": "Rotation around a fixed axis"
        },
        "prismatic": {
            "french": "Glissière",
            "axis_required": True,
            "description": "Translation along a fixed axis"
        },
        "fixed": {
            "french": "Encastrement",
            "axis_required": False,
            "description": "No relative motion"
        },
        "fixed_point": {
            "french": "Appui ponctuel",
            "axis_required": False,
            "description": "Point contact without motion"
        }
    }

    def __init__(self, joint_type, axis=None):
        self.joint_type = joint_type.lower()
        self.axis = axis
        self.K = None
        self.T = None

        self._update_torsors()

    @classmethod
    def list(cls):
        """
        List available mechanical joint types.
        """
        print("Available mechanical joint types:\n")
        for key, info in cls.JOINT_TYPES.items():
            axis_info = "axis required" if info["axis_required"] else "no axis"
            print(f"- {key} ({info['french']}) : {info['description']} [{axis_info}]")

    def _update_torsors(self):
        axis_index = {"x": 0, "y": 1, "z": 2}
        K = np.array([0, 0, 0, 0, 0, 0], dtype=object)

        if self.joint_type not in self.JOINT_TYPES:
            raise ValueError(f"Unknown joint type: {self.joint_type}")

        joint_info = self.JOINT_TYPES[self.joint_type]

        if joint_info["axis_required"]:
            if self.axis is None:
                raise ValueError(
                    f"Axis must be specified for joint type '{self.joint_type}'."
                )
            if self.axis not in axis_index:
                raise ValueError("Axis must be 'x', 'y' or 'z'.")

            idx = axis_index[self.axis]

            if self.joint_type == "revolute":
                K[idx] = 1
            elif self.joint_type == "prismatic":
                K[idx + 3] = 1

        self.K = K

        self.T = np.array([
            None if v is None else (1 if v == 0 else 0)
            for v in self.K
        ], dtype=object)

    def print_torsors(self):
        kinematic_labels = ["Omega_x", "Omega_y", "Omega_z", "V_x", "V_y", "V_z"]
        static_labels = ["M_x", "M_y", "M_z", "F_x", "F_y", "F_z"]

        print(f"Mechanical joint type : {self.joint_type}")
        if self.axis:
            print(f"Axis : {self.axis}")

        print("\nKinematic torsor (DDL):")
        for label, value in zip(kinematic_labels, self.K):
            print(f"  {label} = {value}")

        print("\nStatic torsor (ideal):")
        for label, value in zip(static_labels, self.T):
            print(f"  {label} = {value}")


joint = Joint("prismatic",axis="y")
joint.print_torsors()
joint.list()



