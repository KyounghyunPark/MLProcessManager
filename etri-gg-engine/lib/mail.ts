import { Resend } from "resend"

const mail = new Resend(process.env.RESEND_API_KEY)

export const sendVerificationEmail = async (
  email: string,
  token: string,
) => {
  if (!!process.env.EMAILS_VERIFICATION_DISABLE) {
    return
  }
  const confirmLink = `${process.env.AUTH_URL}/auth/new-verification?token=${token}`
  await mail.emails.send({
    from: `${process.env.EMAILS_FROM_EMAIL}`,
    to: email,
    subject: "Confirm your email",
    html: `<p>Click <a href="${confirmLink}">here</a> to verify your email </p>`
  })
}

export const sendPasswordResetEmail = async (
  email: string,
  token: string
) => {
  if (!!process.env.EMAILS_VERIFICATION_DISABLE) {
    return
  }
  const resetLink = `${process.env.AUTH_URL}/auth/new-password?token=${token}`
  await mail.emails.send({
    from: `${process.env.EMAILS_FROM_EMAIL}`,
    to: email,
    subject: "Reset your password",
    html: `<p>Click <a href="${resetLink}">here</a> to reset your password </p>`
  })
}