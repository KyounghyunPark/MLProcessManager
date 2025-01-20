import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()
async function main() {
  const admin = await prisma.user.upsert({
    where: { email: 'admin@gaion.kr' },
    update: {},
    create: {
      email: 'admin@gaion.kr',
      name: 'Admin',
      password: '$2a$10$fXpNYRM4hVL37aEcheTkGOu2L12w5QqQzyG4hTMXF6XwM.5Pb90kS',
      role: 'ADMIN',
      emailVerified: new Date(),
    },
  })

  const gaion = await prisma.user.upsert({
    where: { email: 'gaion@gaion.kr' },
    update: {},
    create: {
      email: 'gaion@gaion.kr',
      name: 'Gaion',
      password: '$2a$10$fXpNYRM4hVL37aEcheTkGOu2L12w5QqQzyG4hTMXF6XwM.5Pb90kS',
      role: 'USER',
      emailVerified: new Date(),
    },
  })
  console.log({ admin, gaion })
}
main()
  .then(async () => {
    await prisma.$disconnect()
  })
  .catch(async (e) => {
    console.error(e)
    await prisma.$disconnect()
    process.exit(1)
  })