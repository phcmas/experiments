import React from "react"
import "../styles/global.css" // 전역 CSS 파일을 import

function MyApp({ Component, pageProps }) {
  return <Component {...pageProps} />
}

export default MyApp
