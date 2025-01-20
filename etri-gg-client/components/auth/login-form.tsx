"use client"

import * as z from "zod"
import { CardWrapper } from "@/components/auth/card-wrapper";
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { LoginSchema } from "@/schemas";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/form-error";
import { FormSuccess } from "@/components/form-success";
import { login } from "@/actions/login";
import { useState, useTransition } from "react";
import { useSearchParams } from "next/navigation";
import Link from "next/link";

export const LoginForm = () => {
  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    }
  });

  const [isPending, startTransition] = useTransition()
  const [error, setError] = useState<string | undefined>("")
  const [success, setSuccess] = useState<string | undefined>("")
  const searchParams = useSearchParams()
  const urlError = searchParams.get("error") === "OAuthAccountNotLinked" ?
    "Email was already in use with a different provider!" : ""

  const onSubmit = (values: z.infer<typeof LoginSchema>) => {
    console.log(values)
    setSuccess("")
    setError("")

    startTransition(() => {
      login(values)
        .then((data) => {
          setError(data?.error)
          setSuccess(data?.success)
        })
    })

  }

  return (
    <CardWrapper
      headerLabel={""}
      backButtonLabel={"Don't have an account"}
      backButtonHref={"/auth/register"}
      showSocial={false}
    >
      <Form {...form}>
        <form
          onSubmit={form.handleSubmit(onSubmit)}
          className="space-y-6"
        >
          <div>
            <FormField
              name="email"
              control={form.control}
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Email</FormLabel>
                  <FormControl>
                    <Input
                      {...field}
                      disabled={isPending}
                      placeholder={"gaion@gaion.kr"}
                      type={"email"}
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              )}
              />
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
                  <Button size={"sm"} variant={"link"} className={'px-0 font-normal'}>
                    <Link href={"/auth/reset"}>
                      Forgot password?
                    </Link>
                  </Button>
                  <FormMessage />
                </FormItem>
              )}
            />
          </div>

          <FormError message={error || urlError} />
          <FormSuccess message={success} />
          <Button
            type="submit"
            className="w-full"
            disabled={isPending}
          >
            Login
          </Button>
        </form>
      </Form>
    </CardWrapper>
  )
}