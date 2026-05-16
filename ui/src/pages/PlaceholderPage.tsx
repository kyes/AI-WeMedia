import { Construction } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  desc?: string;
}

export default function PlaceholderPage({ title, desc }: PlaceholderPageProps) {
  return (
    <div className="p-6 flex flex-col items-center justify-center min-h-[400px] text-center">
      <Construction size={48} className="text-gray-300 mb-4" />
      <h2 className="text-xl font-semibold text-gray-700">{title}</h2>
      <p className="text-sm text-gray-400 mt-2">{desc || '此页面正在开发中，敬请期待'}</p>
    </div>
  );
}
