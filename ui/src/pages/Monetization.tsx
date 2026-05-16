import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import { DollarSign, TrendingUp, ShoppingBag, BookOpen, Star, ArrowUpRight, Clock, CheckCircle2 } from 'lucide-react';

const revenueData = [
  { month: '11月', 商单收入: 12000, 电商带货: 8500, 知识付费: 3200, 私域变现: 2100 },
  { month: '12月', 商单收入: 15000, 电商带货: 11200, 知识付费: 4500, 私域变现: 2800 },
  { month: '1月', 商单收入: 18000, 电商带货: 13800, 知识付费: 5100, 私域变现: 3200 },
  { month: '2月', 商单收入: 14000, 电商带货: 10500, 知识付费: 4200, 私域变现: 2600 },
  { month: '3月', 商单收入: 21000, 电商带货: 16200, 知识付费: 6800, 私域变现: 4100 },
];

const revenueChannels = [
  { name: '商单合作', value: 45, color: '#3B82F6', amount: '¥21,000' },
  { name: '电商带货', value: 32, color: '#8B5CF6', amount: '¥16,200' },
  { name: '知识付费', value: 15, color: '#10B981', amount: '¥6,800' },
  { name: '私域变现', value: 8, color: '#F59E0B', amount: '¥4,100' },
];

const orders = [
  {
    id: 1,
    brand: '某护肤品牌A',
    type: '商品种草',
    amount: '¥8,500',
    platform: '小红书',
    deadline: '2026-03-25',
    status: 'in_progress',
    match: 96,
  },
  {
    id: 2,
    brand: '某美妆品牌B',
    type: '商品带货',
    amount: '¥12,000',
    platform: '抖音',
    deadline: '2026-03-28',
    status: 'pending',
    match: 92,
  },
  {
    id: 3,
    brand: '某护肤品牌C',
    type: '视频广告',
    amount: '¥18,000',
    platform: '多平台',
    deadline: '2026-04-05',
    status: 'negotiating',
    match: 88,
  },
  {
    id: 4,
    brand: '某日化品牌D',
    type: '直播带货',
    amount: '佣金15%',
    platform: '抖音直播',
    deadline: '2026-03-30',
    status: 'matched',
    match: 85,
  },
];

const statusMap: Record<string, { label: string; color: string }> = {
  in_progress: { label: '进行中', color: 'bg-blue-100 text-blue-700' },
  pending: { label: '待确认', color: 'bg-yellow-100 text-yellow-700' },
  negotiating: { label: '洽谈中', color: 'bg-purple-100 text-purple-700' },
  matched: { label: '新推荐', color: 'bg-green-100 text-green-700' },
  completed: { label: '已完成', color: 'bg-gray-100 text-gray-600' },
};

export default function Monetization() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">商业变现赋能</h1>
          <p className="text-sm text-gray-500 mt-1">多元变现路径管理，实现流量价值最大化</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors">
          <DollarSign size={15} />
          查看变现机会
        </button>
      </div>

      {/* Revenue summary */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: '本月总收入', value: '¥48,100', change: '+28.5%', icon: DollarSign, color: 'bg-green-500' },
          { label: '商单收入', value: '¥21,000', change: '+16.7%', icon: ShoppingBag, color: 'bg-blue-500' },
          { label: '带货佣金', value: '¥16,200', change: '+17.4%', icon: TrendingUp, color: 'bg-purple-500' },
          { label: '知识付费', value: '¥6,800', change: '+33.3%', icon: BookOpen, color: 'bg-orange-500' },
        ].map(metric => {
          const Icon = metric.icon;
          return (
            <div key={metric.label} className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-500">{metric.label}</p>
                  <p className="text-xl font-bold text-gray-900 mt-1">{metric.value}</p>
                </div>
                <div className={`w-9 h-9 ${metric.color} rounded-lg flex items-center justify-center`}>
                  <Icon size={16} className="text-white" />
                </div>
              </div>
              <div className="flex items-center gap-1 mt-2 text-xs text-green-600 font-medium">
                <ArrowUpRight size={12} />
                {metric.change} 较上月
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Revenue trend chart */}
        <div className="lg:col-span-2 bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">变现收入趋势（近5个月）</h3>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={revenueData} margin={{ top: 0, right: 5, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
              <XAxis dataKey="month" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v) => `¥${Number(v).toLocaleString()}`} />
              <Legend />
              <Bar dataKey="商单收入" fill="#3B82F6" radius={[2, 2, 0, 0]} stackId="a" />
              <Bar dataKey="电商带货" fill="#8B5CF6" radius={[2, 2, 0, 0]} stackId="a" />
              <Bar dataKey="知识付费" fill="#10B981" radius={[2, 2, 0, 0]} stackId="a" />
              <Bar dataKey="私域变现" fill="#F59E0B" radius={[2, 2, 0, 0]} stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Revenue channel distribution */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">收入渠道分布</h3>
          <ResponsiveContainer width="100%" height={140}>
            <PieChart>
              <Pie
                data={revenueChannels}
                cx="50%"
                cy="50%"
                innerRadius={40}
                outerRadius={60}
                paddingAngle={3}
                dataKey="value"
              >
                {revenueChannels.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(v) => `${v}%`} />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-2 mt-2">
            {revenueChannels.map(ch => (
              <div key={ch.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: ch.color }}></span>
                  <span className="text-gray-600">{ch.name}</span>
                </div>
                <div className="text-right">
                  <span className="font-bold text-gray-900">{ch.amount}</span>
                  <span className="text-gray-400 ml-1">({ch.value}%)</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Order management */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-gray-900">商单管理</h3>
            <span className="px-2 py-0.5 bg-green-100 text-green-700 text-xs rounded-full font-medium">4个进行中</span>
          </div>
          <button className="text-xs text-blue-600 hover:text-blue-800">查看全部</button>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-xs text-gray-400 border-b border-gray-100 bg-gray-50">
                <th className="text-left py-3 px-5 font-medium">品牌/合作类型</th>
                <th className="text-left py-3 px-4 font-medium">报酬</th>
                <th className="text-left py-3 px-4 font-medium">平台</th>
                <th className="text-left py-3 px-4 font-medium">截止日期</th>
                <th className="text-left py-3 px-4 font-medium">匹配度</th>
                <th className="text-left py-3 px-4 font-medium">状态</th>
                <th className="text-right py-3 px-5 font-medium">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {orders.map(order => {
                const status = statusMap[order.status];
                return (
                  <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                    <td className="py-3 px-5">
                      <div className="text-sm font-medium text-gray-900">{order.brand}</div>
                      <div className="text-xs text-gray-400">{order.type}</div>
                    </td>
                    <td className="py-3 px-4 text-sm font-bold text-green-600">{order.amount}</td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 bg-blue-50 text-blue-700 text-xs rounded-full">{order.platform}</span>
                    </td>
                    <td className="py-3 px-4 text-sm text-gray-600 flex items-center gap-1">
                      <Clock size={12} className="text-gray-400" />
                      {order.deadline}
                    </td>
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="h-1.5 w-16 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-green-500 rounded-full"
                            style={{ width: `${order.match}%` }}
                          />
                        </div>
                        <span className="text-xs font-medium text-green-600">{order.match}%</span>
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 text-xs rounded-full ${status.color}`}>{status.label}</span>
                    </td>
                    <td className="py-3 px-5 text-right">
                      <button className="text-xs text-blue-600 hover:text-blue-800 font-medium">
                        {order.status === 'matched' ? '查看详情' : '管理'}
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {/* Knowledge products */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h3 className="font-semibold text-gray-900 flex items-center gap-2">
            <BookOpen size={16} className="text-orange-500" />
            知识付费产品
          </h3>
          <button className="text-xs text-blue-600 hover:text-blue-800">+ 新建课程</button>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {[
            { title: '护肤小白入门必修课', price: '¥99', sales: 286, revenue: '¥28,314', rating: 4.9 },
            { title: '成分党护肤配方实操课', price: '¥199', sales: 124, revenue: '¥24,676', rating: 4.8 },
            { title: '敏感肌修复21天打卡课', price: '¥149', sales: 198, revenue: '¥29,502', rating: 4.7 },
          ].map((product, i) => (
            <div key={i} className="border border-gray-100 rounded-xl p-4 hover:border-gray-200 transition-colors">
              <div className="flex items-start justify-between mb-2">
                <h4 className="text-sm font-medium text-gray-900 leading-snug">{product.title}</h4>
                <span className="text-lg font-bold text-orange-600 ml-2 flex-shrink-0">{product.price}</span>
              </div>
              <div className="flex items-center justify-between text-xs text-gray-500">
                <span className="flex items-center gap-1"><CheckCircle2 size={11} className="text-green-500" />已售 {product.sales} 份</span>
                <span className="flex items-center gap-1"><Star size={11} className="text-yellow-500 fill-yellow-500" />{product.rating}</span>
              </div>
              <div className="mt-2 pt-2 border-t border-gray-100 flex items-center justify-between">
                <span className="text-xs text-gray-500">累计收入</span>
                <span className="text-sm font-bold text-green-600">{product.revenue}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
