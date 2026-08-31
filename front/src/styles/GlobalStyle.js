import { createGlobalStyle } from "styled-components";


const GlobalStyle = createGlobalStyle`
  * {
    box-sizing: border-box;
  }


  html,
  body,
  #root {
    margin: 0;

    min-width: 320px;
    min-height: 100%;
  }


  body {
    min-height: 100vh;

    font-family:
      Pretendard,
      Inter,
      system-ui,
      -apple-system,
      BlinkMacSystemFont,
      "Segoe UI",
      sans-serif;

    background: #0c0f14;
  }


  button,
  input {
    font: inherit;
  }
`;


export default GlobalStyle;