import { NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import Github from "next-auth/providers/github"
import Google from "next-auth/providers/google"
import { LoginSchema } from "@/schemas";
import { getUserByEmail } from "@/data/user";
import bcrypt from "bcryptjs"

export default {
  providers: [
    Google({
      clientId: process.env.AUTH_GOOGLE_ID,
      clientSecret: process.env.AUTH_GOOGLE_SECRET
    }),
    Github({
      clientId: process.env.AUTH_GITHUB_ID,
      clientSecret: process.env.AUTH_GITHUB_SECRET
    }),
    Credentials({
      async authorize(credentials){
        const validatedFields = LoginSchema.safeParse(credentials)

        if (validatedFields.success){
          const { email, password } = validatedFields.data;
          const user = await getUserByEmail(email)
          if (!user || !user.password) return null;
          const passwordMatch = await bcrypt.compare(
            password,
            user.password
          )

          if (passwordMatch) return user;
        }
        return null;
      }
    })
  ]
} satisfies NextAuthConfig