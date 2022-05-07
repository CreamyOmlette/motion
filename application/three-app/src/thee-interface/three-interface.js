import React, { useEffect, useRef, useState } from "react";
import HandModel from "../handmodel/handmodel";
import ReactDOM from "react-dom";
import { Canvas, useThree } from "@react-three/fiber";
import { Suspense } from "react";
import { Environment } from "@react-three/drei";
import { Controls, useControl } from "react-three-gui";

export default function ThreeInterface({ ...props }) {
  return (
    <Controls.Provider>
      <Controls.Canvas style={{ background: "#171717" }}>
        <ambientLight intensity={1} />
        <spotLight
          intensity={0.5}
          angle={0.2}
          penumbra={1}
          position={[15, 15, 10]}
          castShadow
        />
        <Suspense fallback={null}>
          <HandModel scale={[5, 5, 5]} />
        </Suspense>
      </Controls.Canvas>
      <Controls />
    </Controls.Provider>
  );
}
