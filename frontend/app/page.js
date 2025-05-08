'use client';
import { useEffect, useState } from 'react';
import FileUpload from '../components/FileUpload';

const images = [
  '/foods/aifood1.png',
  '/foods/aifood2.png',
  '/foods/aifood3.png',
  '/foods/aifood4.png',
];

export default function HomePage() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, 6000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative min-h-screen overflow-auto">
      <div
        className="absolute inset-0 z-0 transition-all duration-1000"
        style={{
          backgroundImage: `url(${images[index]})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          minHeight: '100vh',
        }}
      />
      <div className="absolute inset-0 z-0 bg-black/15" />
      <div className="relative z-10 flex flex-col items-center justify-start px-4 py-10 min-h-screen text-white">
        <h1 className="text-3xl md:text-4xl font-bold text-center mb-4 drop-shadow">
          🍱 AI 음식 칼로리 분석기
        </h1>
        <p className="text-center max-w-md text-gray-100 bg-black/30 border border-white/20 p-4 rounded-xl shadow-md backdrop-blur-sm text-sm leading-relaxed mt-4 mb-6">
          업로드한 음식 이미지를 AI가 분석하여 <br />
          <span className="text-green-300 font-semibold">칼로리</span>,
          <span className="text-orange-300 font-semibold"> 탄수화물</span>,
          <span className="text-blue-300 font-semibold"> 단백질</span>,
          <span className="text-purple-300 font-semibold"> 지방</span>을 예측합니다.
          <br />
          <span className="text-pink-400 font-bold underline decoration-pink-300 underline-offset-2">
            다이어트 식단 여부도 함께 확인해보세요!
          </span>
        </p>



        <FileUpload />
      </div>
    </div>
  );
}
