import {
  BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area, Line
} from 'recharts';
import {
  TrendingUp, Users, Eye, Heart, Share2,
  DollarSign, Zap, AlertTriangle, CheckCircle2, ArrowUpRight, ArrowDownRight,
  FileText, BarChart2, Target, Calendar
} from 'lucide-react';

const growthData = [
  { date: '03/14', 粉丝数: 45200, 阅读量: 128000, 互动量: 8200 },
  { date: '03/15', 粉丝数: 46100, 阅读量: 142000, 互动量: 9100 },
  { date: '03/16', 粉丝数: 47500, 阅读量: 135000, 互动量: 7800 },
  { date: '03/17', 粉丝数: 48200, 阅读量: 168000, 互动量: 11200 },
  { date: '03/18', 粉丝数: 49800, 阅读量: 195000, 互动量: 13500 },
  { date: '03/19', 粉丝数: 51200, 阅读量: 182000, 互动量: 12100 },
  { date: '03/20', 粉丝数: 52800, 阅读量: 210000, 互动量: 14800 },
];

const platformData = [
  { platform: '抖音', content: 42, engagement: 58, color: '#000000' },
  { platform: '小红书', content: 28, engagement: 35, color: '#FF2442' },
  { platform: '公众号', content: 15, engagement: 12, color: '#07C160' },
  { platform: '视频号', content: 8, engagement: 9, color: '#576B95' },
  { platform: 'B站', content: 7, engagement: 8, color: '#00AEEC' },
];

const contentTypeData = [
  { name: '干货教程', value: 40, color: '#3B82F6' },
  { name: '产品种草', value: 30, color: '#8B5CF6' },
  { name: '情感共鸣', value: 20, color: '#EC4899' },
  { name: '热点追踪', value: 10, color: '#F59E0B' },
];

const recentAlerts = [
  { type: 'warning', text: '抖音账号粉丝昨日流失加速，流失率较上周上升23%', time: '2小时前' },
  { type: 'success', text: '小红书爆款内容《平价护肤品推荐》互动量突破10万', time: '4小时前' },
  { type: 'info', text: '下周选题日历已生成，共12个选题待确认', time: '6小时前' },
  { type: 'warning', text: '商单"某品牌口红"合作已到截止期，请及时完成内容', time: '1天前' },
];

const topContent = [
  { title: '2024最值得入手的平价护肤品', platform: '小红书', views: '21.5万', likes: '8.2k', revenue: '¥2,300' },
  { title: '抖音带货新手必看：选品技巧分享', platform: '抖音', views: '18.3万', likes: '6.5k', revenue: '¥1,800' },
  { title: '公众号运营从0到10万粉的方法论', platform: '公众号', views: '12.8万', likes: '4.1k', revenue: '¥950' },
  { title: '小红书爆款选题公式大揭秘', platform: '小红书', views: '9.6万', likes: '3.8k', revenue: '¥720' },
];

function StatCard({
  title, value, change, changeType, icon: Icon, color, subtext
}: {
  title: string; value: string; change: string; changeType: 'up' | 'down';
  icon: React.ElementType; color: string; subtext?: string;
}) {
  return (
    <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-500">{title}</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{value}</p>
          {subtext && <p className="text-xs text-gray-400 mt-0.5">{subtext}</p>}
        </div>
        <div className={`w-10 h-10 ${color} rounded-lg flex items-center justify-center`}>
          <Icon size={18} className="text-white" />
        </div>
      </div>
      <div className={`flex items-center gap-1 mt-3 text-xs font-medium ${changeType === 'up' ? 'text-green-600' : 'text-red-500'}`}>
        {changeType === 'up' ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
        <span>{change}</span>
        <span className="text-gray-400 font-normal ml-1">较上周</span>
      </div>
    </div>
  );
}

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">数据概览</h1>
          <p className="text-sm text-gray-500 mt-1">2026年3月20日 · 周五 · 数据更新于 13:02</p>
        </div>
        <div className="flex gap-2">
          <button className="flex items-center gap-2 px-4 py-2 text-sm bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
            <Calendar size={15} />
            <span>近7天</span>
          </button>
          <button className="flex items-center gap-2 px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <BarChart2 size={15} />
            <span>导出报告</span>
          </button>
        </div>
      </div>

      {/* Health Score */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-5 text-white">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-100 text-sm">运营健康度评分</p>
            <div className="flex items-baseline gap-3 mt-1">
              <span className="text-4xl font-bold">82</span>
              <span className="text-blue-200 text-sm">/ 100</span>
            </div>
            <p className="text-blue-100 text-sm mt-1">较上月提升 +5分 · 优秀</p>
          </div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold">91</div>
              <div className="text-blue-200 text-xs mt-1">内容质量</div>
            </div>
            <div>
              <div className="text-2xl font-bold">78</div>
              <div className="text-blue-200 text-xs mt-1">用户增长</div>
            </div>
            <div>
              <div className="text-2xl font-bold">75</div>
              <div className="text-blue-200 text-xs mt-1">商业变现</div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="总粉丝数"
          value="52.8万"
          change="+3.1% (1.6万)"
          changeType="up"
          icon={Users}
          color="bg-blue-500"
          subtext="全平台汇总"
        />
        <StatCard
          title="本周阅读量"
          value="96.1万"
          change="+12.4%"
          changeType="up"
          icon={Eye}
          color="bg-purple-500"
          subtext="7日累计"
        />
        <StatCard
          title="互动总量"
          value="7.67万"
          change="-2.3%"
          changeType="down"
          icon={Heart}
          color="bg-pink-500"
          subtext="点赞+评论+收藏"
        />
        <StatCard
          title="本月变现收入"
          value="¥38,520"
          change="+18.7%"
          changeType="up"
          icon={DollarSign}
          color="bg-green-500"
          subtext="商单+带货+知识付费"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Growth trend */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">增长趋势</h3>
            <div className="flex gap-3 text-xs text-gray-500">
              <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-blue-500 inline-block"></span>粉丝数</span>
              <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-purple-500 inline-block"></span>阅读量</span>
              <span className="flex items-center gap-1"><span className="w-3 h-0.5 bg-pink-500 inline-block"></span>互动量</span>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={growthData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
              <defs>
                <linearGradient id="colorFans" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.1}/>
                  <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
                </linearGradient>
                <linearGradient id="colorReads" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.1}/>
                  <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="date" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Area type="monotone" dataKey="粉丝数" stroke="#3B82F6" fill="url(#colorFans)" strokeWidth={2} />
              <Area type="monotone" dataKey="阅读量" stroke="#8B5CF6" fill="url(#colorReads)" strokeWidth={2} />
              <Line type="monotone" dataKey="互动量" stroke="#EC4899" strokeWidth={2} dot={false} />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Content type distribution */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">内容类型分布</h3>
          <ResponsiveContainer width="100%" height={140}>
            <PieChart>
              <Pie
                data={contentTypeData}
                cx="50%"
                cy="50%"
                innerRadius={45}
                outerRadius={65}
                paddingAngle={3}
                dataKey="value"
              >
                {contentTypeData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-2">
            {contentTypeData.map(item => (
              <div key={item.name} className="flex items-center justify-between text-sm">
                <div className="flex items-center gap-2">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }}></span>
                  <span className="text-gray-600">{item.name}</span>
                </div>
                <span className="font-medium text-gray-900">{item.value}%</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Platform performance + Alerts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Platform performance */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">各平台表现</h3>
            <span className="text-xs text-gray-400">内容占比 vs 互动占比</span>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <BarChart data={platformData} margin={{ top: 0, right: 5, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="platform" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Bar dataKey="content" name="内容占比%" fill="#3B82F6" radius={[3, 3, 0, 0]} />
              <Bar dataKey="engagement" name="互动占比%" fill="#8B5CF6" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Alerts */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">智能预警</h3>
            <span className="text-xs text-blue-600 cursor-pointer hover:underline">全部查看</span>
          </div>
          <div className="space-y-3">
            {recentAlerts.map((alert, index) => (
              <div key={index} className="flex gap-3 text-sm">
                <div className="mt-0.5 flex-shrink-0">
                  {alert.type === 'warning' && <AlertTriangle size={14} className="text-yellow-500" />}
                  {alert.type === 'success' && <CheckCircle2 size={14} className="text-green-500" />}
                  {alert.type === 'info' && <Zap size={14} className="text-blue-500" />}
                </div>
                <div>
                  <p className="text-gray-700 text-xs leading-relaxed">{alert.text}</p>
                  <p className="text-gray-400 text-xs mt-0.5">{alert.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Top Content & Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Top content table */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-semibold text-gray-900">近期热门内容</h3>
            <span className="text-xs text-blue-600 cursor-pointer hover:underline">查看全部</span>
          </div>
          <table className="w-full">
            <thead>
              <tr className="text-xs text-gray-400 border-b border-gray-100">
                <th className="text-left pb-2 font-medium">内容标题</th>
                <th className="text-left pb-2 font-medium">平台</th>
                <th className="text-right pb-2 font-medium">阅读量</th>
                <th className="text-right pb-2 font-medium">互动</th>
                <th className="text-right pb-2 font-medium">收益</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {topContent.map((item, index) => (
                <tr key={index} className="hover:bg-gray-50 transition-colors">
                  <td className="py-2.5 pr-3">
                    <p className="text-sm text-gray-800 truncate max-w-48">{item.title}</p>
                  </td>
                  <td className="py-2.5">
                    <span className="px-2 py-0.5 text-xs bg-blue-50 text-blue-700 rounded-full">{item.platform}</span>
                  </td>
                  <td className="py-2.5 text-right text-sm text-gray-700">{item.views}</td>
                  <td className="py-2.5 text-right text-sm text-gray-700">{item.likes}</td>
                  <td className="py-2.5 text-right text-sm font-medium text-green-600">{item.revenue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Quick actions */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">快捷操作</h3>
          <div className="space-y-2">
            {[
              { icon: Zap, label: 'AI生成今日选题', color: 'bg-blue-50 text-blue-700', badge: '推荐' },
              { icon: FileText, label: '一键生成内容', color: 'bg-purple-50 text-purple-700' },
              { icon: Share2, label: '批量定时发布', color: 'bg-green-50 text-green-700' },
              { icon: Target, label: '运营行动清单', color: 'bg-orange-50 text-orange-700', badge: '3项待完成' },
              { icon: TrendingUp, label: '查看竞品分析', color: 'bg-pink-50 text-pink-700' },
              { icon: DollarSign, label: '商单机会推荐', color: 'bg-yellow-50 text-yellow-700', badge: '5个新商单' },
            ].map((action, index) => {
              const Icon = action.icon;
              return (
                <button
                  key={index}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg ${action.color} hover:opacity-80 transition-opacity text-sm font-medium`}
                >
                  <Icon size={15} />
                  <span className="flex-1 text-left">{action.label}</span>
                  {action.badge && (
                    <span className="text-xs bg-white bg-opacity-70 px-2 py-0.5 rounded-full">{action.badge}</span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
