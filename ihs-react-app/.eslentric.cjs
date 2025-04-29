module.exports = {
    root: true,
    env: { browser: true, es2020: true, node: true },
    extends: [
      'eslint:recommended',
      'plugin:@typescript-eslint/recommended', // Uses TS recommended rules
      'plugin:react/recommended',             // Uses React recommended rules
      'plugin:react/jsx-runtime',             // Supports new JSX transform
      'plugin:react-hooks/recommended',       // Enforces Hooks rules
      'plugin:jsx-a11y/recommended',          // Accessibility rules
      'plugin:tailwindcss/recommended',       // Tailwind rules
      'plugin:prettier/recommended',          // Integrates Prettier with ESLint
    ],
    ignorePatterns: ['dist', '.eslintrc.cjs', 'vite.config.ts', 'postcss.config.js', 'tailwind.config.js'],
    parser: '@typescript-eslint/parser',
    parserOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      project: ['./tsconfig.json', './tsconfig.node.json'], // Point ESLint to your TS config
      tsconfigRootDir: __dirname,
    },
    plugins: ['react-refresh', 'jsx-a11y', 'tailwindcss'],
    settings: {
      react: {
        version: 'detect', // Automatically detect React version
      },
      tailwindcss: {
        // Optional: Set settings if needed, often auto-detected
        // callees: ["cn"], // Recognise custom cn helper
        // config: "tailwind.config.js" // Path to config if not default
      }
    },
    rules: {
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
      'react/prop-types': 'off', // Not needed with TypeScript
      '@typescript-eslint/no-unused-vars': ['warn', { 'argsIgnorePattern': '^_' }], // Warn on unused vars, allowing _ prefix
      'prettier/prettier': ['warn', {}, { usePrettierrc: true }], // Warn on Prettier rules
      'tailwindcss/no-custom-classname': 'off', // Allows custom classnames alongside Tailwind
      'jsx-a11y/anchor-is-valid': 'warn', // Warn about invalid anchors (useful with React Router's Link)
    },
  }