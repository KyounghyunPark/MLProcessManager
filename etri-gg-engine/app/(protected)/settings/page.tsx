"use client"

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { settings } from "@/actions/settings";
import { useState, useTransition } from "react";
import { useSession } from "next-auth/react";
import { useForm } from "react-hook-form";
import * as z from "zod"
import { SettingsSchema } from "@/schemas";
import { zodResolver } from "@hookform/resolvers/zod";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useCurrentUser } from "@/hooks/use-current-user";
import { FormSuccess } from "@/components/form-success";
import { FormError } from "@/components/form-error";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { UserRole } from "@prisma/client";

const SettingsPage = () => {
  const [error, setError] = useState<string | undefined>();
  const [success, setSuccess] = useState<string | undefined>();

  const user = useCurrentUser()
  
  const { update } = useSession();
  const [isPending, startTransition] = useTransition()
  const onSubmit = (values: z.infer<typeof SettingsSchema>) => {
    startTransition (() => {
      settings(values)
        .then((data) =>  {
          if (data.error){
            setError(data.error)
          }
          if (data.success){
            update()
            setSuccess(data.success)
          }
        })
        .catch((error) => {
          setError(error.message)
        })
    })
  }

  const form = useForm<z.infer<typeof SettingsSchema>>({
    resolver: zodResolver(SettingsSchema),
    defaultValues: {
      name: user?.name || undefined,
      email: user?.email || undefined,
      password: undefined,
      newPassword: undefined,
      role: user?.role || undefined,
    }
  });


  return (
    <Card className="w-[600px] mt-2 md:mt-10">
      <CardHeader>
        <p className={'text-2xl font-semibold text-center'}>
          Settings
        </p>
      </CardHeader>
      <CardContent>
        <Form {...form}>
          <form
            className={"space-y-6"}
            onSubmit={form.handleSubmit(onSubmit)}
          >
            <div className={"space-y-4"}>
              <FormField
                control={form.control}
                name={"name"}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input
                        {...field}
                        placeholder={"Gaion"}
                        disabled={isPending}
                      />
                    </FormControl>
                  </FormItem>
                )}
              />
              {/*{user?.isOAuth === false && (*/}
              {/*  <>*/}
              {/*    <FormField*/}
              {/*      control={form.control}*/}
              {/*      name={"email"}*/}
              {/*      render={({ field }) => (*/}
              {/*        <FormItem>*/}
              {/*          <FormLabel>Email</FormLabel>*/}
              {/*          <FormControl>*/}
              {/*            <Input*/}
              {/*              {...field}*/}
              {/*              placeholder={"gaion@gaion.kr"}*/}
              {/*              disabled={isPending}*/}
              {/*              type={"email"}*/}
              {/*            />*/}
              {/*          </FormControl>*/}
              {/*          <FormMessage />*/}
              {/*        </FormItem>*/}
              {/*      )}*/}
              {/*    />*/}
                  {/*<FormField*/}
                  {/*  control={form.control}*/}
                  {/*  name={"password"}*/}
                  {/*  render={({ field }) => (*/}
                  {/*    <FormItem>*/}
                  {/*      <FormLabel>Password</FormLabel>*/}
                  {/*      <FormControl>*/}
                  {/*        <Input*/}
                  {/*          {...field}*/}
                  {/*          placeholder={"******"}*/}
                  {/*          disabled={isPending}*/}
                  {/*          type={"password"}*/}
                  {/*          autoComplete={"none"}*/}
                  {/*        />*/}
                  {/*      </FormControl>*/}
                  {/*      <FormMessage />*/}
                  {/*    </FormItem>*/}
                  {/*  )}*/}
                  {/*/>*/}
                  {/*<FormField*/}
                  {/*  control={form.control}*/}
                  {/*  name={"newPassword"}*/}
                  {/*  render={({ field }) => (*/}
                  {/*    <FormItem>*/}
                  {/*      <FormLabel>New password</FormLabel>*/}
                  {/*      <FormControl>*/}
                  {/*        <Input*/}
                  {/*          {...field}*/}
                  {/*          placeholder={"******"}*/}
                  {/*          disabled={isPending}*/}
                  {/*          type={"password"}*/}
                  {/*          autoComplete={"none"}*/}
                  {/*        />*/}
                  {/*      </FormControl>*/}
                  {/*      <FormMessage />*/}
                  {/*    </FormItem>*/}
                  {/*  )}*/}
                  {/*/>*/}

                  {/*<FormField*/}
                  {/*  control={form.control}*/}
                  {/*  name={"isTwoFactorEnabled"}*/}
                  {/*  render={({ field }) => (*/}
                  {/*    <FormItem className={'flex flex-row items-center justify-between rounded-lg p-3 shadow-sm'}>*/}
                  {/*      <div className={'space-y-0.5'}>*/}
                  {/*        <FormLabel>Two Factor Authentication</FormLabel>*/}
                  {/*        <FormDescription>*/}
                  {/*          Enable two factor authentication for your account*/}
                  {/*        </FormDescription>*/}
                  {/*      </div>*/}
                  {/*      <FormControl>*/}
                  {/*        <Switch*/}
                  {/*          disabled={isPending}*/}
                  {/*          checked={field.value}*/}
                  {/*          onCheckedChange={field.onChange}*/}
                  {/*        />*/}
                  {/*      </FormControl>*/}
                  {/*    </FormItem>*/}
                  {/*  )}*/}
                  {/*>*/}
                  {/*</FormField>*/}
              {/*  </>*/}
              {/*)}*/}

              <FormField
                control={form.control}
                name={"role"}
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Role</FormLabel>
                    <Select
                      disabled={isPending}
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder={"Select a role"}/>
                        </SelectTrigger>
                      </FormControl>
                        <SelectContent>
                          <SelectItem value={UserRole.ADMIN}>
                            Admin
                          </SelectItem>
                          <SelectItem value={UserRole.USER}>
                            User
                          </SelectItem>
                        </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

            </div>
            <FormSuccess message={success} />
            <FormError message={error} />
            <Button type={"submit"} disabled={isPending}>
              Save
            </Button>
          </form>
        </Form>
      </CardContent>
    </Card>
  )
}

export default SettingsPage