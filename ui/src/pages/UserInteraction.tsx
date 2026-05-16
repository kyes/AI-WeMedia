import { Users, Target, Zap, Bell } from 'lucide-react';

const reachStrategies = [
  {
    segment: '核心粉丝',
    channel: '私信 + 社群',
    frequency: '每周2次',
    content: '专属福利、新内容预告、互动话题',
    openRate: '72%',
    color: 'border-blue-200 bg-blue-50',
  },
  {
    segment: '潜在粉丝',
    channel: '评论区引导 + 信息流',
    frequency: '每周3-5次',
    content: '兴趣内容推送、互动引导话术',
    openRate: '38%',
    color: 'border-purple-200 bg-purple-50',
  },
  {
    segment: '流失粉丝',
    channel: '私信召回',
    frequency: '每两周1次',
    content: '专属优惠、召回内容、近期热点摘要',
    openRate: '21%',
    color: 'border-red-200 bg-red-50',
  },
];

const autoReplies = [
  { trigger: '包含"多少钱"', action: '产品价格话术', active: true, used: 1234 },
  { trigger: '包含"怎么买"', action: '购买引导话术', active: true, used: 892 },
  { trigger: '包含"敏感肌"', action: '敏感肌解决方案推荐', active: true, used: 2156 },
  { trigger: '包含"谢谢"', action: '感谢回复模板', active: false, used: 456 },
];

export default function UserInteraction() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">智能互动系统</h1>
        <p className="text-sm text-gray-500 mt-1">分群互动策略管理，自动化互动执行</p>
      </div>

      {/* Reach strategies */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Target size={16} className="text-blue-500" />
          分群触达策略
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {reachStrategies.map(strategy => (
            <div key={strategy.segment} className={`rounded-xl p-4 border ${strategy.color}`}>
              <div className="font-semibold text-gray-900 mb-3">{strategy.segment}</div>
              <div className="space-y-2 text-sm">
                <div className="flex gap-2">
                  <span className="text-gray-500 w-14 flex-shrink-0">渠道</span>
                  <span className="text-gray-800">{strategy.channel}</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-gray-500 w-14 flex-shrink-0">频次</span>
                  <span className="text-gray-800">{strategy.frequency}</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-gray-500 w-14 flex-shrink-0">内容</span>
                  <span className="text-gray-800 leading-relaxed">{strategy.content}</span>
                </div>
                <div className="flex gap-2">
                  <span className="text-gray-500 w-14 flex-shrink-0">打开率</span>
                  <span className="text-green-700 font-medium">{strategy.openRate}</span>
                </div>
              </div>
              <button className="mt-3 w-full py-2 text-xs bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
                编辑策略
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Auto reply */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <Zap size={16} className="text-yellow-500" />
            自动化互动规则
          </h3>
          <button className="text-xs text-blue-600 hover:text-blue-800">+ 添加规则</button>
        </div>
        <div className="space-y-3">
          {autoReplies.map((rule, i) => (
            <div key={i} className="flex items-center gap-4 p-3 border border-gray-100 rounded-xl">
              <div className="flex-1">
                <div className="flex items-center gap-2 text-sm">
                  <span className="bg-yellow-50 text-yellow-700 px-2 py-0.5 rounded text-xs">触发: {rule.trigger}</span>
                  <span className="text-gray-400">→</span>
                  <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded text-xs">回复: {rule.action}</span>
                </div>
              </div>
              <span className="text-xs text-gray-400">已使用 {rule.used} 次</span>
              <div className={`w-10 h-5 rounded-full relative cursor-pointer transition-colors ${rule.active ? 'bg-green-500' : 'bg-gray-200'}`}>
                <div className={`absolute top-0.5 w-4 h-4 bg-white rounded-full shadow transition-all ${rule.active ? 'left-5' : 'left-0.5'}`}></div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Private domain */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Users size={16} className="text-green-500" />
            私域流量沉淀
          </h3>
          <div className="space-y-3">
            {[
              { label: '私域用户总量', value: '8,234', trend: '+12.3%' },
              { label: '企微好友数', value: '3,156', trend: '+8.5%' },
              { label: '社群成员数', value: '5,078', trend: '+15.2%' },
              { label: '私域转化率', value: '6.8%', trend: '+1.2%' },
            ].map(item => (
              <div key={item.label} className="flex items-center justify-between py-2 border-b border-gray-50 last:border-0">
                <span className="text-sm text-gray-600">{item.label}</span>
                <div className="text-right">
                  <span className="text-sm font-bold text-gray-900">{item.value}</span>
                  <span className="text-xs text-green-600 ml-2">{item.trend}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Bell size={16} className="text-purple-500" />
            情绪感知预警
          </h3>
          <div className="space-y-3">
            {[
              { emoji: '😊', sentiment: '正面情绪', pct: 68, color: 'bg-green-500' },
              { emoji: '😐', sentiment: '中性情绪', pct: 24, color: 'bg-gray-400' },
              { emoji: '😠', sentiment: '负面情绪', pct: 8, color: 'bg-red-500' },
            ].map(item => (
              <div key={item.sentiment} className="flex items-center gap-3">
                <span className="text-lg">{item.emoji}</span>
                <span className="text-sm text-gray-700 w-20">{item.sentiment}</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full ${item.color} rounded-full`} style={{ width: `${item.pct}%` }}></div>
                </div>
                <span className="text-sm font-medium text-gray-900">{item.pct}%</span>
              </div>
            ))}
            <div className="mt-2 p-3 bg-yellow-50 rounded-lg border border-yellow-100">
              <p className="text-xs text-yellow-700">检测到今日3条负面评论，AI已自动生成安抚话术，请审核后发送。</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
