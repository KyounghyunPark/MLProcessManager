"use client"

import { usePathname } from "next/navigation";
import { UserButton } from "@/components/auth/user-button";
import { NavigationMenuBar } from "@/app/(protected)/_components/menu-bar";
import React from "react";

export const Navbar = () => {
  const pathname = usePathname()

  return (
    <nav className={'bg-secondary flex justify-between items-center p-2 w-full shadow-md'}>
      <div className={"flex gap-x-2"}>
        <NavigationMenuBar />
      </div>

      <UserButton />
    </nav>
  )
}
