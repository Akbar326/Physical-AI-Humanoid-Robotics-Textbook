import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/">
            Start Learning - 100+ Hours of Content
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="A beginner-friendly, project-based guide to robotics, AI, and humanoid systems">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className={`col col--4 ${styles.moduleCard}`}>
                <h3>Module 1: ROS 2 Fundamentals</h3>
                <p>Master the Robot Operating System with hands-on exercises teaching nodes, publishers, subscribers, services, actions, parameters, and system orchestration.</p>
                <p><strong>⏱️ 18-21 hours</strong></p>
              </div>
              <div className={`col col--4 ${styles.moduleCard}`}>
                <h3>Module 2: Simulation</h3>
                <p>Learn to create physics-based simulations and high-fidelity visualizations. Build robot models, add sensors, and synchronize virtual robots with real physics.</p>
                <p><strong>⏱️ 20-24 hours</strong></p>
              </div>
              <div className={`col col--4 ${styles.moduleCard}`}>
                <h3>Module 3: AI/Isaac</h3>
                <p>Train autonomous robot behaviors using reinforcement learning. Deploy AI models to ROS 2 systems for real-world task execution.</p>
                <p><strong>⏱️ 19-23 hours</strong></p>
              </div>
            </div>
            <div className="row" style={{marginTop: '2rem'}}>
              <div className={`col col--4 col--offset-2 ${styles.moduleCard}`}>
                <h3>Module 4: Vision-Language-Action</h3>
                <p>Integrate vision, language, and action into unified systems. Build robots that respond to natural language commands with end-to-end system integration.</p>
                <p><strong>⏱️ 28-35 hours</strong></p>
              </div>
              <div className={`col col--4 ${styles.whoIsThisFor}`}>
                <h3>Who Is This For?</h3>
                <ul>
                  <li>Complete beginners with no prior robotics experience</li>
                  <li>Python programmers wanting to learn robotics</li>
                  <li>Engineering students looking for hands-on robotics projects</li>
                  <li>Hobbyists interested in robots and AI</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}