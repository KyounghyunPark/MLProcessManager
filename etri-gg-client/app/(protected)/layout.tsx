import React from "react";
import { Navbar } from "@/app/(protected)/_components/navbar";

interface ProtectedLayoutProps {
  children: React.ReactNode
}
const ProtectedLayout = ({ children }: ProtectedLayoutProps) => {
  return (
    <div className={"w-full min-h-full flex flex-col items-center bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-sky-400 to-blue-800"}>
      <Navbar />
      {children}
    </div>
  )
}

export default ProtectedLayout