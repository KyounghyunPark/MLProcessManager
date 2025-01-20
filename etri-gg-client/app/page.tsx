import { Poppins } from "next/font/google"
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LoginButton } from "@/components/auth/login-button";

const font = Poppins({
  subsets: ['latin'],
  weight: ["600"]
})
export default function Home() {
  return (
    <main className={`flex h-full flex-col items-center justify-center 
      bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-sky-400 to-blue-800
      `}>
      <div className="space-y-6 text-center">
        <h1 className={cn("text-6xl font-semibold text-white drop-shadow-md", font.className)}>
          🔐디지털 트윈 데이터 분석 도구
        </h1>
        <p className={'text-white text-lg'}>
          Please login to use the service
        </p>
        <div>
          <LoginButton>
            <Button variant={'secondary'} size={"lg"}>
              Sign in
            </Button>
          </LoginButton>
        </div>
      </div>
    </main>
  );
}

// bg-[radial-gradient(ellipse_at_top, _var(--tw-gradient-stops))] from-sky-400 to-blue-800