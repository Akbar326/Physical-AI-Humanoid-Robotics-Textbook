// @ts-check
// `@type` JSDoc annotations allow editor autocompletion and type checking
// (when paired with `@ts-check`).
// There are various equivalent ways to declare your Docusaurus config.
// See: https://docusaurus.io/docs/api/docusaurus-config

import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI & Humanoid Robotics',
  tagline: 'A Beginner-Friendly Project-Based Guide',
  favicon: 'img/favicon.ico',

  // Set the production url of your site here
  url: 'https://your-github-username.github.io',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'your-github-username', // Usually your GitHub org/username.
  projectName: 'physical-ai-robotics-textbook', // Usually your repo name.
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  // Even if you don't use internalization, you can use this field to set useful
  // metadata like html lang. For example, if your site is Chinese, you may want
  // to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.js',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/your-github-username/physical-ai-robotics-textbook/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      // Replace with your project's social card
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Robotics Textbook',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'textbookSidebar',
            position: 'left',
            label: 'Textbook',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Modules',
            items: [
              {
                label: 'Module 1: ROS 2',
                to: '/docs/module-1/',
              },
              {
                label: 'Module 2: Simulation',
                to: '/docs/module-2/',
              },
              {
                label: 'Module 3: AI/Isaac',
                to: '/docs/module-3/',
              },
              {
                label: 'Module 4: VLA',
                to: '/docs/module-4/',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'GitHub Repository',
                href: 'https://github.com/your-github-username/physical-ai-robotics-textbook',
              },
              {
                label: 'Companion Code Repository',
                href: 'https://github.com/your-github-username/physical-ai-textbook-assets',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'ROS Discourse',
                href: 'https://discourse.ros.org/',
              },
              {
                label: 'Gazebo Community',
                href: 'https://community.gazebosim.org/',
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Physical AI & Humanoid Robotics Textbook. Built with Docusaurus.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
        additionalLanguages: ['python', 'bash', 'yaml', 'json'],
      },
    }),

  plugins: [
    ['@docusaurus/plugin-pwa', {}],
  ],
};

export default config;
