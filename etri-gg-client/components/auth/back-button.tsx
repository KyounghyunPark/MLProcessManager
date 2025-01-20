"use client"

import Link from "next/link";

interface BackButtonProps {
  href: string;
  label: string;
}

import { Button } from "@/components/ui/button";

export const BackButton = ({ href, label } : BackButtonProps) => {
  return (
    <Button
      variant="link"
      className={"w-full font-normal"}
      size={"sm"}
      asChild={true}
    >
      <Link href={href}>
        {label}
      </Link>
    </Button>
  )
}