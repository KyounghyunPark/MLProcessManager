"use server"

import * as z from "zod"
import { RegisterSchema } from "@/schemas";
import bcrypt from 'bcryptjs'
import { db } from "@/lib/db";
import { getUserByEmail } from "@/data/user";
import { generateVerificationToken } from "@/lib/token";
import { sendVerificationEmail } from "@/lib/mail";

export const register = async (values: z.infer<typeof RegisterSchema>) => {
  console.log(values);
  const validatedFields = RegisterSchema.safeParse(values);
  if (!validatedFields.success) {
    return { error: "Invalid fields!" };
  }

  const { email, password, name } = validatedFields.data;
  const hashedPassword = await bcrypt.hash(password, 10);

  const existingUser = await getUserByEmail(email)

  if (existingUser){
    return { error: "Email already in use!" }
  }

  if (!!process.env.EMAILS_VERIFICATION_DISABLE) {
    await db.user.create({
      data: {
        name,
        email,
        password: hashedPassword,
        emailVerified: new Date()
      }
    })

    return { success: "User created successfully!" };
  }

  await db.user.create({
    data: {
      name,
      email,
      password: hashedPassword,
    }
  })

  // TODO: Send verification token email
  const verificationToken = await generateVerificationToken(email)
  await sendVerificationEmail(
    verificationToken.email,
    verificationToken.token
  )

  return { success: "Confirmation email sent!" };
}