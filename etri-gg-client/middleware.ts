import NextAuth from "next-auth";
import authConfig from "@/auth.config";
import { apiAuthPrefix, authRoutes, DEFAULT_LOGIN_REDIRECT, publicRoutes } from "@/routes";

const { auth } = NextAuth(authConfig)

// @ts-expect-error nothing wrong with this
export default auth((req) => {
  const isLoggedIn = !!req.auth
  const { nextUrl } = req

  const isApiAuthRoute = nextUrl.pathname.startsWith(apiAuthPrefix)
  const isPublicRoute = publicRoutes.includes(nextUrl.pathname)
  const isAuthRoute = authRoutes.includes(nextUrl.pathname)

  if (isApiAuthRoute){
    return null
  }

  if (isAuthRoute){
    if (isLoggedIn){
      return Response.redirect(new URL(DEFAULT_LOGIN_REDIRECT, nextUrl))
    }
    return null
  }

  if (!isLoggedIn && !isPublicRoute){
    return Response.redirect(new URL("/auth/login", nextUrl))
  }
  // console.log("ROUTE: ", req.nextUrl.pathname)
  // console.log("Is LOGGED IN: ", isLoggedIn)

  return null
})


export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
};