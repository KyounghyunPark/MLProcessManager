import * as z from "zod"
import { UserRole } from "@prisma/client";

export const LoginSchema = z.object({
  email: z.string().email({
    message: "E-mail is required",
  }),
  password: z.string().min(1, "Password is required"),
})

export const RegisterSchema = z.object({
  email: z.string().email({
    message: "E-mail is required",
  }),
  password: z.string().min(6, "Password is required"),
  name: z.string().min(1, {
    message: "Name is required",
  })
})

export const ResetSchema = z.object({
  email: z.string().email({
    message: "E-mail is required",
  }),
})

export const NewPasswordSchema = z.object({
  password: z.string().min(6, {
    message: "Minimum of 6 characters is required",
  }),
})

export const SettingsSchema = z.object({
  name: z.optional(z.string()),
  isTwoFactorEnabled: z.optional(z.boolean()),
  role: z.enum([UserRole.ADMIN, UserRole.USER]),
  email: z.optional(z.string().email()),
  password: z.optional(z.string().min(6)),
  newPassword: z.optional(z.string().min(6)),
})
// .refine((data) => {
//   if(data.password && !data.newPassword) {
//     return false
//   }
//   return true
// }, {
//   message: "New password is required",
//   path: ["newPassword"]
// })
//   .refine((data) => {
//     if(data.newPassword && !data.password){
//       return false
//     }
//     return true
//   }, {
//     message: "password is required",
//     path: ["password"]
//   })
.refine((data) => {
  if (data.password && data.newPassword && data.password !== data.newPassword) {
    return false
  }
  return true
}, {
  message: "Password does not match",
  path: ["newPassword"]
})