"use server"

import { SettingsSchema } from "@/schemas";
import * as z from "zod"
import { currentUser } from "@/lib/auth";
import { getUserByEmail, getUserById } from "@/data/user";
import { db } from "@/lib/db";
import { generateVerificationToken } from "@/lib/token";
import { sendVerificationEmail } from "@/lib/mail";
import bcrypt from "bcryptjs";

export const settings = async (values: z.infer<typeof SettingsSchema>) => {
  const user = await currentUser()
  if (!user) {
    return { error: "Unauthorized!" }
  }

  const dbUser = await getUserById(user.id!)
  if (!dbUser) {
    return { error: "Unauthorized!" }
  }

  // if (user.isOAuth){
  //   values.email = undefined
  //   values.password = undefined
  //   values.newPassword = undefined
  //   values.isTwoFactorEnabled = undefined
  // }

  if (values.email && values.email !== user.email) {
    const existingUser = await getUserByEmail(values.email)

    if (existingUser && existingUser.id !== user.id) {
      return { error: "Email already in use!" };
    }

    const verificationToken = await generateVerificationToken(values.email)

    await sendVerificationEmail(verificationToken.email, verificationToken.token)
  }

  if (values.password && values.newPassword && dbUser.password) {
    const passwordsMatch = await bcrypt.compare(values.password, dbUser.password)

    if (!passwordsMatch) {
      return { error: "Passwords do not match!" };
    }

    const hashedPassword = await bcrypt.hash(values.newPassword, 10)
    values.password = hashedPassword
    values.newPassword = undefined
  }

  await db.user.update({
    where: { id:dbUser.id },
    data: {
      ...values,
    }
  })

  return { success: "Successfully updated" }
}