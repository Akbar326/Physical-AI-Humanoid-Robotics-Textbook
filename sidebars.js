/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'doc',
      id: 'index',
      label: 'Home',
    },
    {
      type: 'category',
      label: 'Preface & Getting Started',
      items: [
        'preface/about',
        'preface/prerequisites',
        'preface/how-to-use',
        'preface/setup-guide',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 1: ROS 2 Fundamentals',
      items: [
        'module-1/index',
        'module-1/chapter-1-1',
        'module-1/chapter-1-2',
        'module-1/chapter-1-3',
        'module-1/chapter-1-4',
        'module-1/chapter-1-5',
        'module-1/chapter-1-6',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 2: Gazebo Simulation',
      items: [
        'module-2/index',
        'module-2/chapter-2-1',
        'module-2/chapter-2-2',
        'module-2/chapter-2-3',
        'module-2/chapter-2-4',
        'module-2/chapter-2-5',
        'module-2/chapter-2-6',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 3: Isaac Sim & AI Integration',
      items: [
        'module-3/index',
        'module-3/chapter-3-1',
        'module-3/chapter-3-2',
        'module-3/chapter-3-3',
        'module-3/chapter-3-4',
        'module-3/chapter-3-5',
      ],
      collapsed: false,
    },
    {
      type: 'category',
      label: 'Module 4: Vision-Language-Action Models',
      items: [
        'module-4/index',
        'module-4/chapter-4-1',
        'module-4/chapter-4-2',
        'module-4/chapter-4-3',
        'module-4/chapter-4-4',
        'module-4/chapter-4-5',
        'module-4/chapter-4-6',
      ],
      collapsed: false,
    },
  ],
};

module.exports = sidebars;
