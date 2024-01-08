import React from 'react';
import { Link } from 'preact-router';
import styles from './style.module.css';

export default function Td({ children, to }) {
  const ContentTag = to ? Link : 'div';

  return (
    <td className={styles.td}>
      <ContentTag href={to}>{children}</ContentTag>
    </td>
  );
}