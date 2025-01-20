import { hash } from "bcryptjs";

export default function saltAndHashPassword(unHashPass: string){
  return hash(unHashPass, 10).then(function (hashedPassword: string) {
    return hashedPassword;
  })
}