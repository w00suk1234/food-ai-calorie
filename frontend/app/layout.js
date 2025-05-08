import '../styles/globals.css';

export const metadata = {
  title: 'AI 음식 분석기',
  description: 'Next.js 기반 식단 분석기',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
