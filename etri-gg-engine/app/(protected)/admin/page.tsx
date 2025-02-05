"use client"

import { Card, CardContent, CardHeader } from "@/components/ui/card";
import { RoleGate } from "@/components/auth/role-gate";
import { FormSuccess } from "@/components/form-success";
import { UserRole } from "@prisma/client";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { admin } from "@/actions/admin";

const AdminPage = () => {

  const onApiRouteClick = () => {
    fetch("/api/admin")
      .then((res) => {
        if(res.status === 200) {
          toast.success("ok");
        } else {
          toast.error("Forbidden");
        }
      })
  }
  const onServerActionClick = () => {
    admin()
      .then((data) => {
        if (data.error){
          toast.error(data.error)
        }
        if (data.success){
          toast.success(data.success);
        }
      })
  }

  return (
    <Card className="w-[600px]">
      <CardHeader>
        <p className={''}>
          Admin
        </p>
      </CardHeader>
      <CardContent>
        <RoleGate allowedRole={UserRole.ADMIN}>
          <FormSuccess message={'You are allowed to see this content'}/>
        </RoleGate>
        <div className={'flex flex-row items-center justify-between rounded-md border p-3 shadow-md'}>
          <p className={'text-sm font-medium'}>
            Admin-only API Route
          </p>
          <Button onClick={onApiRouteClick}>
            Click to test
          </Button>
        </div>
        <div className={'flex flex-row items-center justify-between rounded-md border p-3 shadow-md'}>
          <p className={'text-sm font-medium'}>
            Admin-only Server Action
          </p>
          <Button onClick={onServerActionClick}>
            Click to test
          </Button>
        </div>
      </CardContent>
    </Card>
  )
}

export default AdminPage