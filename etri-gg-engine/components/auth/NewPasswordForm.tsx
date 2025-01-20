"use client"

import * as z from "zod"
import { CardWrapper } from "@/components/auth/card-wrapper";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { NewPasswordSchema } from "@/schemas";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/form-error";
import { FormSuccess } from "@/components/form-success";
import { useState, useTransition } from "react";
import { newPassword } from "@/actions/new-password";
import { useSearchParams } from "next/navigation";

export const NewPasswordForm = () => {
  const searchParams = useSearchParams()
  const token = searchParams.get("token")
  
  const form = useForm<z.infer<typeof NewPasswordSchema>>({
    resolver: zodResolver(NewPasswordSchema),
    defaultValues: {
      password: "",
    }
  });

  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | undefined>("")
  const [success, setSuccess] = useState<string | undefined>("")

  const onSubmit = (values: z.infer<typeof NewPasswordSchema>) => {
    console.log(values)
    setSuccess("")
    setError("")
    startTransition(() => {
      newPassword(values, token)
        .then((data)=>{
          setError(data?.error)
          setSuccess(data?.success)
        })
    })

  }

  return (
    <CardWrapper
      headerLabel={"Enter your new password?"}
      backButtonLabel={"Back to login"}
      backButtonHref={"/auth/login"}
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-6"
        >
          <div>
            <FormField
              name="password"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Password</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      disabled={isPending}
                      placeholder={"******"}
                      type={"password"}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormError message={error} />
          <FormSuccess message={success} />
          <Button
            type="submit"
            className="w-full"
            disabled={isPending}
          >
            Reset password
          </Button>
        </form>
      </Form>
    </CardWrapper>
  )
}