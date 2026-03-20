import { Activity, Shield, AlertTriangle, CheckCircle2, Eye, Users, BarChart2 } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const healthData = [
  { date: '3/14', score: 78 },
  { date: '3/15', score: 80 },
  { date: '3/16', score: 79 },
  { date: '3/17', score: 82 },
  { date: '3/18', score: 85 },
  { date: '3/19', score: 83 },
  { date: '3/20', score: 82 },
];

export default function Monitor() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">运营监控</h1>
        <p className="text-sm text-gray-500 mt-1">内容、用户、数据全维度实时监控</p>
      </div>

      {/* Health score trend */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Activity size={16} className="text-blue-500" />
          账号健康度趋势（7日）
        </h3>
        <ResponsiveContainer width="100%" height={180}>
          <LineChart data={healthData} margin={{ top: 5, right: 5, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f5f5f5" />
            <XAxis dataKey="date" tick={{ fontSize: 11 }} />
            <YAxis domain={[60, 100]} tick={{ fontSize: 11 }} />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#3B82F6" strokeWidth={2} dot={{ fill: '#3B82F6' }} />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Content monitoring */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Eye size={16} className="text-purple-500" />
            内容运营监控
          </h3>
          <div className="space-y-3">
            {[
              { label: '内容质量均分', value: 88, status: 'good', note: '优秀' },
              { label: '原创度均分', value: 85, status: 'good', note: '良好' },
              { label: '合规通过率', value: 98, status: 'excellent', note: '优秀' },
              { label: '周发布完成率', value: 92, status: 'good', note: '7/7篇完成' },
            ].map(item => (
              <div key={item.label} className="flex items-center gap-3">
                <span className="text-sm text-gray-600 w-28">{item.label}</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${item.status === 'excellent' ? 'bg-green-500' : 'bg-blue-500'}`}
                    style={{ width: `${item.value}%` }} />
                </div>
                <span className="text-sm font-bold text-gray-900">{item.value}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${item.status === 'excellent' ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'}`}>
                  {item.note}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* User monitoring */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Users size={16} className="text-green-500" />
            用户运营监控
          </h3>
          <div className="space-y-3">
            {[
              { label: '7日留存率', value: 68, status: 'medium', note: '待提升' },
              { label: '30日留存率', value: 45, status: 'warning', note: '注意' },
              { label: '粉丝互动率', value: 4.0, isPercent: true, status: 'good', note: '良好' },
              { label: '用户满意度', value: 91, status: 'excellent', note: '优秀' },
            ].map(item => (
              <div key={item.label} className="flex items-center gap-3">
                <span className="text-sm text-gray-600 w-28">{item.label}</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${
                    item.status === 'excellent' ? 'bg-green-500' :
                    item.status === 'good' ? 'bg-blue-500' :
                    item.status === 'warning' ? 'bg-yellow-500' :
                    'bg-orange-500'
                  }`} style={{ width: `${item.isPercent ? item.value * 10 : item.value}%` }} />
                </div>
                <span className="text-sm font-bold text-gray-900">{item.value}{item.isPercent ? '%' : ''}</span>
                <span className={`text-xs px-2 py-0.5 rounded-full ${
                  item.status === 'excellent' ? 'bg-green-100 text-green-700' :
                  item.status === 'good' ? 'bg-blue-100 text-blue-700' :
                  item.status === 'warning' ? 'bg-yellow-100 text-yellow-700' :
                  'bg-orange-100 text-orange-700'
                }`}>{item.note}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Security monitoring */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <Shield size={16} className="text-red-500" />
            账号安全监控
          </h3>
          <div className="space-y-3">
            {[
              { item: '账号违规风险', status: 'safe', desc: '无违规记录', color: 'text-green-600' },
              { item: '内容限流状态', status: 'safe', desc: '正常推流', color: 'text-green-600' },
              { item: '粉丝异常波动', status: 'warning', desc: '昨日流失率+0.3%', color: 'text-yellow-600' },
              { item: '敏感词检测', status: 'safe', desc: '本周0次触发', color: 'text-green-600' },
            ].map(item => (
              <div key={item.item} className="flex items-center justify-between py-1.5 border-b border-gray-50 last:border-0">
                <span className="text-sm text-gray-700">{item.item}</span>
                <div className="flex items-center gap-2">
                  <span className={`text-xs ${item.color}`}>{item.desc}</span>
                  {item.status === 'safe'
                    ? <CheckCircle2 size={14} className="text-green-500" />
                    : <AlertTriangle size={14} className="text-yellow-500" />
                  }
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Data monitoring */}
        <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
          <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
            <BarChart2 size={16} className="text-orange-500" />
            核心数据监控
          </h3>
          <div className="space-y-3">
            {[
              { metric: '日均曝光量', value: '15.8万', target: '20万', pct: 79, status: 'medium' },
              { metric: '互动率', value: '4.0%', target: '5%', pct: 80, status: 'medium' },
              { metric: '转化率', value: '2.8%', target: '3.5%', pct: 80, status: 'medium' },
              { metric: '变现ROI', value: '3.2x', target: '3x', pct: 100, status: 'excellent' },
            ].map(item => (
              <div key={item.metric} className="flex items-center gap-3">
                <span className="text-sm text-gray-600 w-20">{item.metric}</span>
                <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div className={`h-full rounded-full ${item.status === 'excellent' ? 'bg-green-500' : 'bg-blue-500'}`}
                    style={{ width: `${item.pct}%` }} />
                </div>
                <span className="text-sm font-bold text-gray-900">{item.value}</span>
                <span className="text-xs text-gray-400">/ {item.target}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
