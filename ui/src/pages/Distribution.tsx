import { useState } from 'react';
import { Clock, CheckCircle2, Circle, Play, Pause, Plus, Edit2, Globe, AlertTriangle } from 'lucide-react';

const platforms = [
  { name: '抖音', icon: '🎵', color: 'bg-black text-white', bestTime: '12:00, 20:00-22:00' },
  { name: '小红书', icon: '📕', color: 'bg-red-500 text-white', bestTime: '12:00-13:00, 21:00-23:00' },
  { name: '公众号', icon: '💬', color: 'bg-green-500 text-white', bestTime: '08:00, 20:00-22:00' },
  { name: '视频号', icon: '📹', color: 'bg-blue-500 text-white', bestTime: '12:00, 19:00-21:00' },
  { name: 'B站', icon: '📺', color: 'bg-cyan-500 text-white', bestTime: '18:00-22:00' },
];

const scheduledPosts = [
  {
    id: 1,
    title: '素人护肤博主必看！平价护肤成分解析',
    platforms: ['抖音', '小红书'],
    scheduledTime: '2026-03-20 20:00',
    status: 'scheduled',
    thumbnail: '🌿',
    type: '图文',
  },
  {
    id: 2,
    title: '敏感肌护肤误区大盘点（避坑指南）',
    platforms: ['公众号', '小红书'],
    scheduledTime: '2026-03-21 12:00',
    status: 'draft',
    thumbnail: '⚠️',
    type: '长图文',
  },
  {
    id: 3,
    title: '国货精华横评：30款实测真实体验',
    platforms: ['抖音', '视频号', 'B站'],
    scheduledTime: '2026-03-22 19:30',
    status: 'scheduled',
    thumbnail: '💊',
    type: '视频',
  },
  {
    id: 4,
    title: '春季换季护肤全攻略',
    platforms: ['小红书', '公众号'],
    scheduledTime: '2026-03-24 21:00',
    status: 'pending_review',
    thumbnail: '🌸',
    type: '图文',
  },
];

const statusMap: Record<string, { label: string; color: string; icon: React.ElementType }> = {
  scheduled: { label: '已排期', color: 'bg-green-100 text-green-700', icon: CheckCircle2 },
  draft: { label: '草稿', color: 'bg-gray-100 text-gray-600', icon: Edit2 },
  pending_review: { label: '待审核', color: 'bg-yellow-100 text-yellow-700', icon: Circle },
  published: { label: '已发布', color: 'bg-blue-100 text-blue-700', icon: Globe },
};

export default function Distribution() {
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(['抖音', '小红书', '公众号']);

  const togglePlatform = (name: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(name) ? prev.filter(p => p !== name) : [...prev, name]
    );
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">跨平台智能分发</h1>
          <p className="text-sm text-gray-500 mt-1">智能适配各平台内容格式，最优时间批量发布</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <Plus size={15} />
          新建发布任务
        </button>
      </div>

      {/* Platform selection */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4">平台管理</h3>
        <div className="grid grid-cols-2 lg:grid-cols-5 gap-3">
          {platforms.map(platform => (
            <div
              key={platform.name}
              onClick={() => togglePlatform(platform.name)}
              className={`cursor-pointer rounded-xl p-4 border-2 transition-all ${
                selectedPlatforms.includes(platform.name)
                  ? 'border-blue-400 bg-blue-50'
                  : 'border-gray-100 bg-gray-50 opacity-60'
              }`}
            >
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xl">{platform.icon}</span>
                <span className="font-medium text-sm text-gray-900">{platform.name}</span>
                {selectedPlatforms.includes(platform.name) && (
                  <CheckCircle2 size={14} className="text-blue-500 ml-auto" />
                )}
              </div>
              <div className="text-xs text-gray-500">
                <Clock size={11} className="inline mr-1" />
                最佳时间: {platform.bestTime}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Schedule queue */}
        <div className="lg:col-span-2 bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
          <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
            <h3 className="font-semibold text-gray-900">发布队列</h3>
            <span className="text-xs text-gray-400">{scheduledPosts.length} 个待发布</span>
          </div>
          <div className="divide-y divide-gray-50">
            {scheduledPosts.map(post => {
              const statusInfo = statusMap[post.status];
              const StatusIcon = statusInfo.icon;
              return (
                <div key={post.id} className="p-4 hover:bg-gray-50 transition-colors">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center text-xl flex-shrink-0">
                      {post.thumbnail}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h4 className="text-sm font-medium text-gray-900 truncate">{post.title}</h4>
                        <span className={`flex-shrink-0 flex items-center gap-1 px-2 py-0.5 text-xs rounded-full ${statusInfo.color}`}>
                          <StatusIcon size={11} />
                          {statusInfo.label}
                        </span>
                      </div>
                      <div className="flex items-center gap-3 mt-1.5">
                        <div className="flex gap-1">
                          {post.platforms.map(p => (
                            <span key={p} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">{p}</span>
                          ))}
                        </div>
                        <span className="text-xs text-gray-400">{post.type}</span>
                      </div>
                      <div className="flex items-center gap-1 mt-1 text-xs text-gray-500">
                        <Clock size={11} />
                        {post.scheduledTime}
                      </div>
                    </div>
                    <div className="flex gap-2 flex-shrink-0">
                      <button className="p-1.5 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors">
                        <Edit2 size={14} />
                      </button>
                      <button className="p-1.5 text-gray-400 hover:text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                        <Play size={14} />
                      </button>
                      <button className="p-1.5 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors">
                        <Pause size={14} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Best time recommendations */}
        <div className="space-y-4">
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Clock size={16} className="text-blue-500" />
              最优发布时间
            </h3>
            <div className="space-y-3">
              {[
                { platform: '抖音', times: ['12:00', '20:00', '21:30'], heat: [85, 92, 78] },
                { platform: '小红书', times: ['12:30', '21:00', '22:30'], heat: [72, 88, 80] },
                { platform: '公众号', times: ['08:00', '20:30'], heat: [65, 90] },
              ].map(item => (
                <div key={item.platform} className="border border-gray-100 rounded-lg p-3">
                  <div className="text-sm font-medium text-gray-800 mb-2">{item.platform}</div>
                  <div className="flex gap-2">
                    {item.times.map((time, i) => (
                      <div
                        key={time}
                        className={`flex-1 text-center py-1.5 rounded-lg text-xs font-medium ${
                          item.heat[i] >= 85
                            ? 'bg-green-100 text-green-700'
                            : item.heat[i] >= 70
                            ? 'bg-yellow-100 text-yellow-700'
                            : 'bg-gray-100 text-gray-600'
                        }`}
                      >
                        {time}
                        <div className="text-xs font-normal opacity-70 mt-0.5">热度{item.heat[i]}</div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Content adaptation */}
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">内容适配状态</h3>
            <div className="space-y-2">
              {[
                { platform: '抖音', status: 'done', note: '字幕已生成' },
                { platform: '小红书', status: 'done', note: '封面已优化' },
                { platform: '公众号', status: 'processing', note: '格式转换中...' },
                { platform: '视频号', status: 'pending', note: '等待处理' },
                { platform: 'B站', status: 'warning', note: '标题超长，需修改' },
              ].map(item => (
                <div key={item.platform} className="flex items-center gap-3 py-1.5">
                  <span className="text-sm text-gray-700 w-16">{item.platform}</span>
                  <div className="flex-1">
                    <div className="text-xs text-gray-500">{item.note}</div>
                  </div>
                  <span className={`w-2 h-2 rounded-full ${
                    item.status === 'done' ? 'bg-green-500' :
                    item.status === 'processing' ? 'bg-blue-500 animate-pulse' :
                    item.status === 'warning' ? 'bg-yellow-500' :
                    'bg-gray-300'
                  }`}></span>
                </div>
              ))}
            </div>
            {/* Warning */}
            <div className="mt-3 p-2.5 bg-yellow-50 rounded-lg border border-yellow-100 flex items-start gap-2">
              <AlertTriangle size={13} className="text-yellow-600 mt-0.5 flex-shrink-0" />
              <p className="text-xs text-yellow-700">B站标题超过80字限制，请前往编辑页面修改标题。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
