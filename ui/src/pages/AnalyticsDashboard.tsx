import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, AreaChart, Area, Line
} from 'recharts';
import {
  TrendingUp, TrendingDown, Eye, Heart, Users, DollarSign,
  AlertTriangle, FileDown, Play, ArrowUpRight, ArrowDownRight,
  Search
} from 'lucide-react';

const dailyData = [
  { date: '3/14', 阅读量: 128000, 互动量: 8200, 粉丝净增: 820, 收入: 3200 },
  { date: '3/15', 阅读量: 142000, 互动量: 9100, 粉丝净增: 950, 收入: 2800 },
  { date: '3/16', 阅读量: 135000, 互动量: 7800, 粉丝净增: 710, 收入: 3100 },
  { date: '3/17', 阅读量: 168000, 互动量: 11200, 粉丝净增: 1150, 收入: 4200 },
  { date: '3/18', 阅读量: 195000, 互动量: 13500, 粉丝净增: 1580, 收入: 5600 },
  { date: '3/19', 阅读量: 182000, 互动量: 12100, 粉丝净增: 1320, 收入: 4800 },
  { date: '3/20', 阅读量: 210000, 互动量: 14800, 粉丝净增: 1620, 收入: 6100 },
];

const platformCompare = [
  { platform: '抖音', 曝光量: 85000, 互动率: 6.8, 转化率: 3.2, 粉丝增长: 850 },
  { platform: '小红书', 曝光量: 62000, 互动率: 8.5, 转化率: 4.1, 粉丝增长: 620 },
  { platform: '公众号', 曝光量: 38000, 互动率: 4.2, 转化率: 2.8, 粉丝增长: 280 },
  { platform: '视频号', 曝光量: 15000, 互动率: 3.1, 转化率: 1.9, 粉丝增长: 150 },
  { platform: 'B站', 曝光量: 10000, 互动率: 5.8, 转化率: 2.5, 粉丝增长: 120 },
];

const contentAttribution = [
  { factor: '标题吸引力', impact: 35, trend: 'up' },
  { factor: '封面点击率', impact: 28, trend: 'up' },
  { factor: '发布时间', impact: 18, trend: 'neutral' },
  { factor: '内容质量', impact: 12, trend: 'up' },
  { factor: '话题标签', impact: 7, trend: 'down' },
];

const alerts = [
  { level: 'high', metric: '抖音粉丝流失率', current: '1.8%', threshold: '1.5%', change: '+0.3%', desc: '粉丝流失加速，建议发布用户召回内容' },
  { level: 'medium', metric: '小红书互动率', current: '8.5%', threshold: '6%', change: '+2.5%', desc: '互动率超过预期，内容质量表现优秀' },
  { level: 'low', metric: '公众号阅读量', current: '3.8万', threshold: '5万', change: '-24%', desc: '阅读量低于预期，建议优化推送时间和标题策略' },
];

export default function AnalyticsDashboard() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">实时数据看板</h1>
          <p className="text-sm text-gray-500 mt-1">全平台数据聚合监控，实时更新</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 px-3 py-2 text-sm border border-gray-200 bg-white rounded-lg hover:bg-gray-50">
            <Play size={13} />
            实时模式
          </button>
          <button className="flex items-center gap-2 px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            <FileDown size={13} />
            导出报告
          </button>
        </div>
      </div>

      {/* Alert banner */}
      <div className="space-y-2">
        {alerts.map((alert, i) => (
          <div
            key={i}
            className={`flex items-center gap-3 px-4 py-3 rounded-xl border text-sm ${
              alert.level === 'high' ? 'bg-red-50 border-red-200' :
              alert.level === 'medium' ? 'bg-green-50 border-green-200' :
              'bg-yellow-50 border-yellow-200'
            }`}
          >
            <AlertTriangle size={15} className={
              alert.level === 'high' ? 'text-red-500' :
              alert.level === 'medium' ? 'text-green-500' :
              'text-yellow-500'
            } />
            <span className="font-medium text-gray-800">{alert.metric}:</span>
            <span className={`font-bold ${alert.level === 'high' ? 'text-red-700' : alert.level === 'medium' ? 'text-green-700' : 'text-yellow-700'}`}>
              {alert.current}
            </span>
            <span className="text-gray-500">（阈值: {alert.threshold}）</span>
            <span className="text-gray-500">{alert.desc}</span>
          </div>
        ))}
      </div>

      {/* Key metrics */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: '今日曝光量', value: '21.0万', change: '+15.4%', up: true, icon: Eye, color: 'text-blue-500 bg-blue-50' },
          { label: '今日互动量', value: '14,800', change: '+22.3%', up: true, icon: Heart, color: 'text-pink-500 bg-pink-50' },
          { label: '今日净增粉', value: '+1,620', change: '+8.7%', up: true, icon: Users, color: 'text-purple-500 bg-purple-50' },
          { label: '今日变现收入', value: '¥6,100', change: '+27.1%', up: true, icon: DollarSign, color: 'text-green-500 bg-green-50' },
        ].map(metric => {
          const Icon = metric.icon;
          return (
            <div key={metric.label} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <p className="text-xs text-gray-500">{metric.label}</p>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${metric.color}`}>
                  <Icon size={15} />
                </div>
              </div>
              <p className="text-xl font-bold text-gray-900">{metric.value}</p>
              <div className={`flex items-center gap-1 mt-1.5 text-xs font-medium ${metric.up ? 'text-green-600' : 'text-red-500'}`}>
                {metric.up ? <ArrowUpRight size={12} /> : <ArrowDownRight size={12} />}
                <span>{metric.change}</span>
                <span className="text-gray-400 font-normal">较昨日</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Main chart */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">7日数据趋势</h3>
          <div className="flex gap-2">
            {['日', '周', '月'].map(period => (
              <button
                key={period}
                className={`px-3 py-1 text-xs rounded-lg transition-colors ${
                  period === '日' ? 'bg-blue-600 text-white' : 'border border-gray-200 text-gray-500 hover:bg-gray-50'
                }`}
              >
                {period}
              </button>
            ))}
          </div>
        </div>
        <ResponsiveContainer width="100%" height={220}>
          <AreaChart data={dailyData} margin={{ top: 5, right: 5, left: -10, bottom: 0 }}>
            <defs>
              <linearGradient id="colorRead" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.15}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
              </linearGradient>
              <linearGradient id="colorFans" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.15}/>
                <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis tick={{ fontSize: 11 }} />
            <Tooltip />
            <Legend />
            <Area type="monotone" dataKey="阅读量" stroke="#3B82F6" fill="url(#colorRead)" strokeWidth={2} />
            <Area type="monotone" dataKey="互动量" stroke="#8B5CF6" fill="url(#colorFans)" strokeWidth={2} />
            <Line type="monotone" dataKey="粉丝净增" stroke="#10B981" strokeWidth={2} dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Platform comparison */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">各平台数据对比</h3>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={platformCompare} margin={{ top: 0, right: 5, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
              <XAxis dataKey="platform" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="互动率" fill="#3B82F6" radius={[3, 3, 0, 0]} />
              <Bar dataKey="转化率" fill="#8B5CF6" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Attribution analysis */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">内容效果归因分析</h3>
          <div className="space-y-3">
            {contentAttribution.map(item => (
              <div key={item.factor} className="flex items-center gap-3">
                <span className="text-sm text-gray-700 w-28 flex-shrink-0">{item.factor}</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-blue-500 rounded-full"
                    style={{ width: `${item.impact * 2.5}%` }}
                  />
                </div>
                <span className="text-sm font-bold text-gray-900 w-10 text-right">{item.impact}%</span>
                <span className="text-xs">
                  {item.trend === 'up' && <TrendingUp size={14} className="text-green-500" />}
                  {item.trend === 'down' && <TrendingDown size={14} className="text-red-500" />}
                  {item.trend === 'neutral' && <span className="text-gray-400">-</span>}
                </span>
              </div>
            ))}
          </div>
          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
            <p className="text-xs text-blue-700">
              💡 <strong>优化建议：</strong>标题吸引力对曝光影响最大（35%），建议重点优化标题文案，尝试使用数字+痛点+解决方案的公式。
            </p>
          </div>
        </div>
      </div>

      {/* Competitor comparison */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900">竞品对标分析</h3>
          <div className="flex gap-2">
            <div className="relative">
              <Search size={14} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
              <input className="pl-8 pr-3 py-1.5 text-xs border border-gray-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-400" placeholder="添加竞品账号..." />
            </div>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-xs text-gray-400 border-b border-gray-100">
                <th className="text-left pb-2 font-medium">账号</th>
                <th className="text-right pb-2 font-medium">粉丝数</th>
                <th className="text-right pb-2 font-medium">周更量</th>
                <th className="text-right pb-2 font-medium">平均互动</th>
                <th className="text-right pb-2 font-medium">互动率</th>
                <th className="text-right pb-2 font-medium">对比</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {[
                { name: '🟢 我的账号', fans: '52.8万', weekly: 7, avgInteraction: '2,114', rate: '4.0%', diff: 'self' },
                { name: '竞品A - 护肤研究所', fans: '68.5万', weekly: 9, avgInteraction: '2,740', rate: '4.0%', diff: 'equal' },
                { name: '竞品B - 成分说', fans: '45.2万', weekly: 5, avgInteraction: '1,357', rate: '3.0%', diff: 'better' },
                { name: '竞品C - 平价护肤日记', fans: '82.1万', weekly: 12, avgInteraction: '3,284', rate: '4.0%', diff: 'worse' },
              ].map((row, i) => (
                <tr key={i} className={`${row.diff === 'self' ? 'bg-blue-50' : 'hover:bg-gray-50'} transition-colors`}>
                  <td className="py-2.5 font-medium text-gray-900">{row.name}</td>
                  <td className="py-2.5 text-right text-gray-700">{row.fans}</td>
                  <td className="py-2.5 text-right text-gray-700">{row.weekly}篇</td>
                  <td className="py-2.5 text-right text-gray-700">{row.avgInteraction}</td>
                  <td className="py-2.5 text-right text-gray-700">{row.rate}</td>
                  <td className="py-2.5 text-right">
                    {row.diff === 'self' && <span className="text-xs px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full">本账号</span>}
                    {row.diff === 'better' && <span className="text-xs px-2 py-0.5 bg-green-100 text-green-700 rounded-full">领先</span>}
                    {row.diff === 'worse' && <span className="text-xs px-2 py-0.5 bg-red-100 text-red-700 rounded-full">落后</span>}
                    {row.diff === 'equal' && <span className="text-xs px-2 py-0.5 bg-gray-100 text-gray-600 rounded-full">持平</span>}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
