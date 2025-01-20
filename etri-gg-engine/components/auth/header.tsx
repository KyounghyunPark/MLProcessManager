import { Poppins } from "next/font/google";
import { cn } from "@/lib/utils";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"]
})

interface HeaderProps {
  label: string
}

export const Header = ({ label }: HeaderProps) => {
  return (
    <div className={"w-full flex flex-col gap-y-4 items-center justify-center"}>
      <h1 className={cn("text-3xl font-semibold", font.className)}>
        디지털 트윈 데이터 분석 도구
      </h1>
      <p className={"text-muted-foreground text-sm"}>
        {label}
      </p>
    </div>
  )
}