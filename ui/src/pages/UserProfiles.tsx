import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import { Users, UserCheck, UserMinus, MessageCircle, Target, Filter } from 'lucide-react';

const userSegments = [
  { name: '核心粉丝', value: 12, color: '#3B82F6', desc: '高互动高转化', count: '6.3万' },
  { name: '潜在粉丝', value: 35, color: '#8B5CF6', desc: '低互动高潜力', count: '18.5万' },
  { name: '泛粉', value: 38, color: '#D1D5DB', desc: '低价值', count: '20.1万' },
  { name: '流失粉丝', value: 15, color: '#F87171', desc: '高沉睡', count: '7.9万' },
];

const ageData = [
  { age: '18-24', percent: 28 },
  { age: '25-30', percent: 35 },
  { age: '31-35', percent: 22 },
  { age: '36-40', percent: 10 },
  { age: '40+', percent: 5 },
];

const genderData = [
  { name: '女性', value: 78, color: '#EC4899' },
  { name: '男性', value: 22, color: '#3B82F6' },
];

const users = [
  { id: 1, avatar: '小', name: '小美同学', segment: '核心粉丝', tags: ['敏感肌', '25-30岁', '精华控', '高消费'], interactions: 248, lastActive: '今天', value: 'high' },
  { id: 2, avatar: '云', name: '护肤云云', segment: '核心粉丝', tags: ['油皮', '18-24岁', '平价党'], interactions: 186, lastActive: '昨天', value: 'high' },
  { id: 3, avatar: '南', name: '南南爱美丽', segment: '潜在粉丝', tags: ['干皮', '31-35岁', '品质生活'], interactions: 42, lastActive: '3天前', value: 'medium' },
  { id: 4, avatar: '阳', name: '阳光护肤记', segment: '流失粉丝', tags: ['混合肌', '30-35岁'], interactions: 3, lastActive: '2个月前', value: 'low' },
  { id: 5, avatar: '苗', name: '苗苗日记', segment: '潜在粉丝', tags: ['油皮', '学生', '平价好物'], interactions: 68, lastActive: '5天前', value: 'medium' },
];

function SegmentBadge({ segment }: { segment: string }) {
  const map: Record<string, string> = {
    '核心粉丝': 'bg-blue-100 text-blue-700',
    '潜在粉丝': 'bg-purple-100 text-purple-700',
    '泛粉': 'bg-gray-100 text-gray-600',
    '流失粉丝': 'bg-red-100 text-red-700',
  };
  return <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${map[segment] || 'bg-gray-100 text-gray-600'}`}>{segment}</span>;
}

export default function UserProfiles() {
  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">用户画像构建</h1>
          <p className="text-sm text-gray-500 mt-1">实时分析全平台用户数据，智能构建用户画像</p>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
          <Target size={15} />
          生成触达方案
        </button>
      </div>

      {/* Segment cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {userSegments.map(seg => {
          const icons: Record<string, React.ElementType> = {
            '核心粉丝': UserCheck,
            '潜在粉丝': Users,
            '泛粉': Users,
            '流失粉丝': UserMinus,
          };
          const Icon = icons[seg.name] || Users;
          return (
            <div key={seg.name} className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-3">
                <div className="w-9 h-9 rounded-lg flex items-center justify-center" style={{ backgroundColor: seg.color + '20' }}>
                  <Icon size={16} style={{ color: seg.color }} />
                </div>
                <span className="text-2xl font-bold" style={{ color: seg.color }}>{seg.value}%</span>
              </div>
              <div className="text-sm font-medium text-gray-900">{seg.name}</div>
              <div className="text-xs text-gray-500 mt-0.5">{seg.desc}</div>
              <div className="text-xs text-gray-400 mt-1">共 {seg.count} 人</div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Segment pie chart */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">用户分层分布</h3>
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Pie data={userSegments} cx="50%" cy="50%" outerRadius={65} dataKey="value" paddingAngle={2}>
                {userSegments.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip formatter={(value) => `${value}%`} />
            </PieChart>
          </ResponsiveContainer>
          <div className="space-y-1.5 mt-2">
            {userSegments.map(seg => (
              <div key={seg.name} className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full" style={{ backgroundColor: seg.color }}></span>
                  <span className="text-gray-600">{seg.name}</span>
                </div>
                <span className="text-gray-800 font-medium">{seg.count}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Age distribution */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">年龄分布</h3>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={ageData} margin={{ top: 0, right: 5, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="age" tick={{ fontSize: 11 }} />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip formatter={(v) => `${v}%`} />
              <Bar dataKey="percent" fill="#8B5CF6" radius={[3, 3, 0, 0]} name="占比%" />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 flex items-center gap-4 text-sm">
            {genderData.map(g => (
              <div key={g.name} className="flex items-center gap-2">
                <span className="w-3 h-3 rounded-full" style={{ backgroundColor: g.color }}></span>
                <span className="text-gray-600">{g.name}</span>
                <span className="font-bold text-gray-900">{g.value}%</span>
              </div>
            ))}
          </div>
        </div>

        {/* Interest tags */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4">兴趣标签云</h3>
          <div className="flex flex-wrap gap-2">
            {[
              { tag: '护肤', size: 'text-lg', weight: 'font-bold' },
              { tag: '平价好物', size: 'text-base', weight: 'font-semibold' },
              { tag: '敏感肌', size: 'text-base', weight: 'font-semibold' },
              { tag: '成分党', size: 'text-sm', weight: 'font-medium' },
              { tag: '干皮', size: 'text-sm', weight: 'font-medium' },
              { tag: '油皮', size: 'text-sm', weight: 'font-medium' },
              { tag: '抗衰老', size: 'text-sm', weight: '' },
              { tag: '素颜感', size: 'text-xs', weight: '' },
              { tag: '国货', size: 'text-xs', weight: '' },
              { tag: '精华', size: 'text-sm', weight: 'font-medium' },
              { tag: '防晒', size: 'text-xs', weight: '' },
              { tag: '美白', size: 'text-xs', weight: '' },
              { tag: '控油', size: 'text-xs', weight: '' },
              { tag: '修复屏障', size: 'text-xs', weight: '' },
            ].map((item, i) => (
              <span
                key={item.tag}
                className={`px-2.5 py-1 rounded-full ${item.size} ${item.weight} ${
                  i < 3 ? 'bg-blue-100 text-blue-700' :
                  i < 6 ? 'bg-purple-100 text-purple-700' :
                  'bg-gray-100 text-gray-600'
                }`}
              >
                {item.tag}
              </span>
            ))}
          </div>

          <div className="mt-4 pt-4 border-t border-gray-100">
            <h4 className="text-xs font-medium text-gray-500 mb-2">消费能力分布</h4>
            <div className="space-y-1.5">
              {[
                { label: '高消费（500+/月）', pct: 18 },
                { label: '中消费（200-500）', pct: 45 },
                { label: '低消费（200以下）', pct: 37 },
              ].map(item => (
                <div key={item.label}>
                  <div className="flex justify-between text-xs text-gray-500 mb-0.5">
                    <span>{item.label}</span>
                    <span>{item.pct}%</span>
                  </div>
                  <div className="h-1.5 bg-gray-100 rounded-full">
                    <div className="h-full bg-blue-400 rounded-full" style={{ width: `${item.pct}%` }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* User list */}
      <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
          <h3 className="font-semibold text-gray-900">用户列表</h3>
          <div className="flex gap-2">
            <button className="flex items-center gap-2 px-3 py-1.5 text-sm border border-gray-200 rounded-lg hover:bg-gray-50">
              <Filter size={13} />
              筛选
            </button>
          </div>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="text-xs text-gray-400 border-b border-gray-100 bg-gray-50">
                <th className="text-left py-3 px-5 font-medium">用户</th>
                <th className="text-left py-3 px-4 font-medium">分层</th>
                <th className="text-left py-3 px-4 font-medium">标签</th>
                <th className="text-right py-3 px-4 font-medium">互动次数</th>
                <th className="text-right py-3 px-4 font-medium">最近活跃</th>
                <th className="text-right py-3 px-5 font-medium">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {users.map(user => (
                <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-3 px-5">
                    <div className="flex items-center gap-3">
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        {user.avatar}
                      </div>
                      <span className="text-sm font-medium text-gray-900">{user.name}</span>
                    </div>
                  </td>
                  <td className="py-3 px-4">
                    <SegmentBadge segment={user.segment} />
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex flex-wrap gap-1">
                      {user.tags.slice(0, 3).map(tag => (
                        <span key={tag} className="px-1.5 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">{tag}</span>
                      ))}
                    </div>
                  </td>
                  <td className="py-3 px-4 text-right">
                    <span className={`text-sm font-medium ${user.value === 'high' ? 'text-green-600' : user.value === 'medium' ? 'text-blue-600' : 'text-gray-400'}`}>
                      {user.interactions}
                    </span>
                  </td>
                  <td className="py-3 px-4 text-right text-sm text-gray-500">{user.lastActive}</td>
                  <td className="py-3 px-5 text-right">
                    <button className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1 ml-auto">
                      <MessageCircle size={12} />
                      发送互动
                    </button>
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
