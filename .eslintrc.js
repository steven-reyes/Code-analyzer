// .eslintrc.js
module.exports = {
    env: {
      browser: true, // if front-end code
      es2021: true,
      node: true
    },
    extends: [
      "eslint:recommended",
      "plugin:react/recommended",  // If you're using React
      "plugin:@typescript-eslint/recommended" // If using TypeScript
    ],
    parser: "@typescript-eslint/parser", // if using TypeScript
    parserOptions: {
      ecmaVersion: "latest",
      sourceType: "module"
    },
    plugins: [
      "react",
      "@typescript-eslint"
    ],
    rules: {
      // Examples of custom rules
      "no-unused-vars": "warn",
      "react/prop-types": "off"  // if using TypeScript for React props
    }
  };
  