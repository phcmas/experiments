import dotenv from "dotenv"

const allowedNodeEnvs = ["local", "test", "live"]
if (allowedNodeEnvs.includes(process.env.NODE_ENV) === false) {
  throw new Error(`NODE_ENV must be one of ${allowedNodeEnvs.join(", ")}. Current value: ${process.env.NODE_ENV}`)
}

dotenv.config({ path: `../../.env.${process.env.NODE_ENV}` })

const nextConfig = {
  reactStrictMode: false,
  publicRuntimeConfig: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
    USER_ID: process.env.USER_ID,
  },
}

export default nextConfig
