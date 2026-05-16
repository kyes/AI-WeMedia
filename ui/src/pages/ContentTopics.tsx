import { useState } from 'react';
import {
  Lightbulb, TrendingUp, Search, Filter, Star,
  BarChart2, Zap, CheckCircle, Plus, Tag,
  AlertTriangle, RefreshCw
} from 'lucide-react';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Tooltip } from 'recharts';

const topics = [
  {
    id: 1,
    title: '2026年最值得入手的平价护肤成分解析',
    score: 94,
    heat: 92,
    competition: 35,
    match: 98,
    commercial: 88,
    source: '百度指数',
    tags: ['护肤', '平价', '成分'],
    status: 'recommended',
    predictViews: '15-25万',
    predictEngagement: '4.5-6.5%',
  },
  {
    id: 2,
    title: '敏感肌护肤误区大盘点（避坑指南）',
    score: 89,
    heat: 78,
    competition: 45,
    match: 95,
    commercial: 85,
    source: '粉丝评论',
    tags: ['敏感肌', '护肤误区', '干货'],
    status: 'recommended',
    predictViews: '10-18万',
    predictEngagement: '5.2-7.1%',
  },
  {
    id: 3,
    title: '春季过敏护肤全攻略：从预防到修复',
    score: 86,
    heat: 88,
    competition: 52,
    match: 82,
    commercial: 79,
    source: '抖音热点',
    tags: ['春季', '过敏', '护肤'],
    status: 'saved',
    predictViews: '8-15万',
    predictEngagement: '3.8-5.5%',
  },
  {
    id: 4,
    title: '素人如何通过护肤博主月入5万？变现路径分享',
    score: 82,
    heat: 85,
    competition: 68,
    match: 78,
    commercial: 95,
    source: '微博热搜',
    tags: ['变现', '护肤博主', '经验分享'],
    status: 'pending',
    predictViews: '12-20万',
    predictEngagement: '6.1-8.3%',
  },
  {
    id: 5,
    title: '国货护肤品实测：30款平价精华横评',
    score: 79,
    heat: 74,
    competition: 40,
    match: 91,
    commercial: 92,
    source: '行业数据库',
    tags: ['国货', '精华', '横评'],
    status: 'pending',
    predictViews: '9-16万',
    predictEngagement: '4.2-5.8%',
  },
];

const radarData = [
  { dimension: '传播热度', value: 92 },
  { dimension: '竞争度', value: 65 },
  { dimension: '账号匹配', value: 98 },
  { dimension: '商业价值', value: 88 },
  { dimension: '可行性', value: 85 },
];

const accountStages = [
  { label: '冷启动期', active: false },
  { label: '成长期', active: true },
  { label: '成熟期', active: false },
  { label: '衰退期', active: false },
];

export default function ContentTopics() {
  const [selectedTopic, setSelectedTopic] = useState(topics[0]);
  const [activeTab, setActiveTab] = useState<'topics' | 'positioning' | 'calendar'>('topics');

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600 bg-green-50';
    if (score >= 80) return 'text-blue-600 bg-blue-50';
    return 'text-yellow-600 bg-yellow-50';
  };

  const getStatusBadge = (status: string) => {
    const map: Record<string, { label: string; color: string }> = {
      recommended: { label: 'AI推荐', color: 'bg-blue-100 text-blue-700' },
      saved: { label: '已收藏', color: 'bg-green-100 text-green-700' },
      pending: { label: '待确认', color: 'bg-yellow-100 text-yellow-700' },
    };
    const item = map[status] || { label: status, color: 'bg-gray-100 text-gray-600' };
    return <span className={`px-2 py-0.5 text-xs rounded-full ${item.color}`}>{item.label}</span>;
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">智能选题引擎</h1>
          <p className="text-sm text-gray-500 mt-1">AI实时分析热点，为您精准推荐高潜力选题</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <RefreshCw size={15} />
          <span>刷新选题库</span>
        </button>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 bg-gray-100 p-1 rounded-lg w-fit">
        {[
          { key: 'topics', label: '选题库' },
          { key: 'positioning', label: '账号定位' },
          { key: 'calendar', label: '选题日历' },
        ].map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key as typeof activeTab)}
            className={`px-4 py-1.5 text-sm rounded-md transition-colors ${
              activeTab === tab.key ? 'bg-white text-gray-900 font-medium shadow-sm' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {activeTab === 'topics' && (
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {/* Topic list */}
          <div className="lg:col-span-3 space-y-3">
            {/* Filters */}
            <div className="flex gap-3 items-center">
              <div className="flex-1 relative">
                <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                <input
                  type="text"
                  placeholder="搜索选题..."
                  className="w-full pl-9 pr-4 py-2 text-sm border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <button className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                <Filter size={15} />
                <span>筛选</span>
              </button>
              <button className="flex items-center gap-2 px-3 py-2 text-sm bg-blue-50 text-blue-700 border border-blue-200 rounded-lg hover:bg-blue-100 transition-colors">
                <Zap size={15} />
                <span>AI生成更多</span>
              </button>
            </div>

            {/* Topics */}
            <div className="space-y-2">
              {topics.map(topic => (
                <div
                  key={topic.id}
                  onClick={() => setSelectedTopic(topic)}
                  className={`bg-white rounded-xl p-4 border cursor-pointer transition-all ${
                    selectedTopic.id === topic.id
                      ? 'border-blue-300 shadow-md shadow-blue-50'
                      : 'border-gray-100 hover:border-gray-200 shadow-sm'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`text-center px-2.5 py-1.5 rounded-lg font-bold text-sm min-w-[52px] ${getScoreColor(topic.score)}`}>
                      <div className="text-lg leading-tight">{topic.score}</div>
                      <div className="text-xs font-normal opacity-70">综合分</div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between gap-2">
                        <h3 className="text-sm font-medium text-gray-900 leading-snug">{topic.title}</h3>
                        {getStatusBadge(topic.status)}
                      </div>
                      <div className="flex items-center gap-3 mt-2 text-xs text-gray-500">
                        <span className="flex items-center gap-1">
                          <TrendingUp size={12} />热度 {topic.heat}
                        </span>
                        <span className="flex items-center gap-1">
                          <BarChart2 size={12} />竞争 {topic.competition}
                        </span>
                        <span className="flex items-center gap-1">
                          <Tag size={12} />来源: {topic.source}
                        </span>
                      </div>
                      <div className="flex flex-wrap gap-1.5 mt-2">
                        {topic.tags.map(tag => (
                          <span key={tag} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded-full">{tag}</span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Topic detail */}
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <div className="flex items-start justify-between">
                <h3 className="font-semibold text-gray-900 text-sm">选题详情分析</h3>
                <Lightbulb size={16} className="text-yellow-500 mt-0.5" />
              </div>
              <p className="text-sm text-gray-700 mt-3 leading-relaxed">{selectedTopic.title}</p>

              <div className="grid grid-cols-2 gap-3 mt-4">
                <div className="bg-blue-50 rounded-lg p-3 text-center">
                  <div className="text-lg font-bold text-blue-700">{selectedTopic.predictViews}</div>
                  <div className="text-xs text-blue-500 mt-0.5">预测曝光量</div>
                </div>
                <div className="bg-purple-50 rounded-lg p-3 text-center">
                  <div className="text-lg font-bold text-purple-700">{selectedTopic.predictEngagement}</div>
                  <div className="text-xs text-purple-500 mt-0.5">预测互动率</div>
                </div>
              </div>

              {/* Radar chart */}
              <div className="mt-4">
                <p className="text-xs text-gray-500 mb-2">多维评分分析</p>
                <ResponsiveContainer width="100%" height={160}>
                  <RadarChart data={radarData}>
                    <PolarGrid />
                    <PolarAngleAxis dataKey="dimension" tick={{ fontSize: 10 }} />
                    <Radar dataKey="value" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.15} />
                    <Tooltip />
                  </RadarChart>
                </ResponsiveContainer>
              </div>

              <div className="flex gap-2 mt-4">
                <button className="flex-1 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium">
                  确认选题
                </button>
                <button className="flex-1 py-2 text-sm border border-gray-200 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors">
                  生成内容
                </button>
              </div>
            </div>

            {/* Quick stats */}
            <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <h3 className="font-semibold text-gray-900 text-sm mb-3">评分维度</h3>
              <div className="space-y-3">
                {[
                  { label: '传播热度', value: selectedTopic.heat, color: 'bg-red-500' },
                  { label: '账号匹配', value: selectedTopic.match, color: 'bg-blue-500' },
                  { label: '商业潜力', value: selectedTopic.commercial, color: 'bg-green-500' },
                  { label: '竞争程度', value: 100 - selectedTopic.competition, color: 'bg-yellow-500', label2: `竞争度: ${selectedTopic.competition}` },
                ].map(item => (
                  <div key={item.label}>
                    <div className="flex justify-between text-xs text-gray-600 mb-1">
                      <span>{item.label2 || item.label}</span>
                      <span className="font-medium">{item.value}</span>
                    </div>
                    <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        className={`h-full ${item.color} rounded-full transition-all`}
                        style={{ width: `${item.value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'positioning' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Account stage */}
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">账号阶段评估</h3>
            <div className="flex gap-3 mb-6">
              {accountStages.map(stage => (
                <div
                  key={stage.label}
                  className={`flex-1 text-center py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    stage.active
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-500'
                  }`}
                >
                  {stage.label}
                </div>
              ))}
            </div>
            <div className="bg-blue-50 rounded-lg p-4 border border-blue-100">
              <div className="flex items-center gap-2 mb-2">
                <CheckCircle size={16} className="text-blue-600" />
                <span className="text-sm font-medium text-blue-900">当前处于：成长期</span>
              </div>
              <p className="text-sm text-blue-700">粉丝规模42-60万，内容稳定输出，互动率良好。建议重点提升内容深度与商业化转化效率，加大差异化竞争优势。</p>
            </div>
            <div className="mt-4 space-y-3">
              <h4 className="text-sm font-medium text-gray-700">当前阶段运营建议</h4>
              {[
                '加大垂直领域深度内容产出，巩固账号专业定位',
                '建立私域流量池，开始布局商业化变现',
                '强化与核心粉丝的互动，提升用户粘性',
                '优化内容矩阵，差异化定位强化品牌识别度',
              ].map((tip, i) => (
                <div key={i} className="flex items-start gap-2 text-sm text-gray-600">
                  <span className="w-5 h-5 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-xs flex-shrink-0 mt-0.5">{i + 1}</span>
                  {tip}
                </div>
              ))}
            </div>
          </div>

          {/* Domain positioning */}
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4">领域细分定位</h3>
            <div className="space-y-3">
              {[
                { path: '美妆 → 护肤 → 敏感肌护理 → 平价好物', score: 95, recommended: true },
                { path: '美妆 → 护肤 → 成分党 → 功效分析', score: 88, recommended: true },
                { path: '美妆 → 彩妆 → 日常通勤妆', score: 72, recommended: false },
                { path: '生活方式 → 自律 → 护肤习惯养成', score: 68, recommended: false },
              ].map((item, i) => (
                <div key={i} className={`flex items-center justify-between p-3 rounded-lg border ${item.recommended ? 'border-blue-200 bg-blue-50' : 'border-gray-100 bg-gray-50'}`}>
                  <div className="flex items-center gap-2">
                    {item.recommended && <Star size={14} className="text-blue-500 fill-blue-500" />}
                    <span className="text-sm text-gray-800">{item.path}</span>
                  </div>
                  <span className={`text-sm font-bold ${item.recommended ? 'text-blue-700' : 'text-gray-500'}`}>{item.score}</span>
                </div>
              ))}
            </div>
            <div className="mt-4 p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-start gap-2">
                <AlertTriangle size={14} className="text-yellow-600 mt-0.5" />
                <p className="text-xs text-yellow-700">检测到近期3篇内容偏离账号定位（彩妆领域），建议回归核心护肤方向以维持定位一致性。</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'calendar' && (
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">本周选题日历</h3>
            <div className="flex gap-2">
              <button className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">上一周</button>
              <button className="px-3 py-1.5 text-sm bg-blue-600 text-white rounded-lg">本周</button>
              <button className="px-3 py-1.5 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">下一周</button>
            </div>
          </div>
          <div className="grid grid-cols-7 gap-2">
            {['周一', '周二', '周三', '周四', '周五', '周六', '周日'].map((day, i) => (
              <div key={day} className="text-center">
                <div className="text-xs text-gray-500 mb-2">{day}</div>
                <div className={`rounded-lg p-2 min-h-[100px] border ${i === 4 ? 'border-blue-300 bg-blue-50' : 'border-gray-100 bg-gray-50'}`}>
                  {i === 0 && (
                    <div className="text-xs bg-blue-600 text-white rounded p-1.5 leading-tight">
                      敏感肌护肤误区盘点
                    </div>
                  )}
                  {i === 2 && (
                    <div className="text-xs bg-green-600 text-white rounded p-1.5 leading-tight">
                      国货精华横评测
                    </div>
                  )}
                  {i === 4 && (
                    <div className="text-xs bg-purple-600 text-white rounded p-1.5 leading-tight">
                      平价护肤成分解析（今日）
                    </div>
                  )}
                  {i === 6 && (
                    <div className="text-xs bg-yellow-600 text-white rounded p-1.5 leading-tight">
                      春季过敏护肤攻略
                    </div>
                  )}
                  <button className="w-full mt-1 text-xs text-gray-400 hover:text-gray-600">
                    <Plus size={12} className="mx-auto" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
