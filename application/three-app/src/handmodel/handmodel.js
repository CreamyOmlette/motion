import React, { useEffect, useRef, useState } from "react";
import { useGLTF } from "@react-three/drei";
import { useThree, useFrame } from "@react-three/fiber";
import { Controls, useControl } from "react-three-gui";
import "./hand.css";
const deg2rad = (degrees) => degrees * (Math.PI / 180);

export default function HandModel({ ...props }) {
  const [state, set_state] = useState(true);
  const [flexion_wrist, set_flex_wrist] = useState(0);
  const [flexion_index, set_flex_index] = useState(0);
  const [flexion_middle, set_flex_middle] = useState(0);
  const [flexion_ring, set_flex_ring] = useState(0);
  const [flexion_little, set_flex_little] = useState(0);
  const [flexion_thumb, set_flex_thumb] = useState(0);
  const [clicked, set_clicked] = useState(false);
  const [name, set_name] = useState("");
  useThree(({ camera }) => {
    camera.rotation.set(deg2rad(10), deg2rad(-10), deg2rad(0));
  });
  const group = useRef();
  const { nodes, materials } = useGLTF("/handv2.gltf");
  const flex_index = (level) => {
    nodes.index.rotation.y = 0.8;
    nodes.index.rotation.x = level <= 50 ? 0.03 * level : 1.5;
    nodes.index.children[0].rotation.z = level > 50 ? 0.5 : 0;
    nodes.index.children[0].rotation.x =
      level > 50 ? (level <= 75 ? (level - 50) * 0.04 : 1) : 0;
    nodes.index.children[0].children[0].rotation.z = level > 75 ? 0.2 : 0;
    nodes.index.children[0].children[0].rotation.x =
      level > 75 ? (level - 75) * 0.04 : 0;
  };
  const flex_middle = (level) => {
    nodes.middle.rotation.y = 0.8;
    nodes.middle.rotation.x = level <= 50 ? 0.032 * level : 1.6;

    nodes.middle.children[0].rotation.z = level > 50 ? 0.8 : 0;
    nodes.middle.children[0].rotation.x =
      level > 50 ? (level <= 75 ? (level - 50) * 0.072 : 1.8) : 0;

    nodes.middle.children[0].children[0].rotation.z = level > 75 ? 0.2 : 0;
    nodes.middle.children[0].children[0].rotation.x =
      level > 75 ? (level - 75) * 0.04 : 0;
  };
  const flex_ring = (level) => {
    nodes.ring.rotation.y = 0.8;
    nodes.ring.rotation.x = level <= 50 ? 0.032 * level : 1.6;

    nodes.ring.children[0].rotation.z = level > 50 ? 0.8 : 0;
    nodes.ring.children[0].rotation.x =
      level > 50 ? (level <= 75 ? (level - 50) * 0.072 : 1.8) : 0;

    nodes.ring.children[0].children[0].rotation.z = level > 75 ? 0.2 : 0;
    nodes.ring.children[0].children[0].rotation.x =
      level > 75 ? (level - 75) * 0.04 : 0;
  };
  const flex_little = (level) => {
    nodes.little.rotation.y = 0.8;
    nodes.little.rotation.x = level <= 50 ? 0.032 * level : 1.6;

    nodes.little.children[0].rotation.z = level > 50 ? 0.8 : 0;
    nodes.little.children[0].rotation.x =
      level > 50 ? (level <= 75 ? (level - 50) * 0.072 : 1.8) : 0;

    nodes.little.children[0].children[0].rotation.z = level > 75 ? 0.2 : 0;
    nodes.little.children[0].children[0].rotation.x =
      level > 75 ? (level - 75) * 0.04 : 0;
  };
  const flex_thumb = (level) => {
    nodes.thumb.rotation.y = 0.8;
    nodes.thumb.rotation.x = level <= 75 ? 0.02 * level : 1.5;

    nodes.thumb.children[0].rotation.z = level > 75 ? 0.8 : 0;
    nodes.thumb.children[0].rotation.x = level > 75 ? 0.012 * (level - 75) : 0;
  };
  const flex_wrist = (level) => {
    nodes.Wrist.rotation.x = (level - 30) * 0.02;
  };
  const wrist_flexion = useControl("Wrist", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_wrist, set_flex_wrist],
  });
  const index_flexion = useControl("Index", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_index, set_flex_index],
  });
  const middle_flexion = useControl("Middle", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_middle, set_flex_middle],
  });
  const ring_flexion = useControl("Ring", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_ring, set_flex_ring],
  });
  const little_flexion = useControl("Little", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_little, set_flex_little],
  });
  const thumb_flexion = useControl("Thumb", {
    type: "number",
    max: 100,
    min: 0,
    state: [flexion_thumb, set_flex_thumb],
  });

  const preset_name = useControl("Name", {
    type: "string",
    value: "",
    state: [name, set_name],
    onChange: (e) => {
      set_name(e);
    },
  });

  const button = useControl("Save Preset", {
    type: "button",
    onClick: () => set_clicked(true),
  });
  const handleClick = () => {
    console.log(name);
    console.log({
      flexion_wrist,
      flexion_index,
      flexion_middle,
      flexion_little,
      flexion_ring,
      flexion_thumb,
    });
  };
  useFrame(() => {
    if (group.current) {
      group.current.rotation.y = 4.5;
      group.current.rotation.x = -0.6;
      group.current.position.y = -2.5;
      group.current.position.z = -2;
      // console.log(wrist_flexion);
      // set_flex(state ? flexion + 1 : flexion - 1);
      // nodes.index.rotation.y = 0.8;
      // nodes.index.rotation.x += state ? 0.01 : -0.01;
      // if (flexion >= 99) {
      //   set_state(false);
      // }
      // if (flexion <= 1) {
      //   set_state(true);
      // }
    }
  });
  useEffect(() => {
    flex_wrist(flexion_wrist);
    flex_index(flexion_index);
    flex_middle(flexion_middle);
    flex_ring(flexion_ring);
    flex_little(flexion_little);
    flex_thumb(flexion_thumb);
  }, [
    flexion_wrist,
    flexion_index,
    flexion_middle,
    flexion_little,
    flexion_ring,
    flexion_thumb,
  ]);

  useEffect(() => {
    if (clicked) {
      handleClick();
      set_clicked(false);
    }
  }, [clicked]);

  return (
    <group ref={group} {...props} dispose={null}>
      <group position={[0.18, 0.62, -0.32]} scale={0.19}>
        <primitive object={nodes.Bone} />
        <skinnedMesh
          geometry={nodes.Plane005.geometry}
          material={materials["Material #46"]}
          skeleton={nodes.Plane005.skeleton}
        />
      </group>
    </group>
  );
}

useGLTF.preload("/handv2.gltf");
