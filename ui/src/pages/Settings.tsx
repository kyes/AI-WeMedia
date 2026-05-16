import { User, Bell, Palette, Shield, Lock, Save } from 'lucide-react';
import { useState } from 'react';

export default function SystemSettings() {
  const [activeTab, setActiveTab] = useState('account');

  const tabs = [
    { key: 'account', label: '账号偏好', icon: User },
    { key: 'notifications', label: '通知配置', icon: Bell },
    { key: 'appearance', label: '界面个性化', icon: Palette },
    { key: 'security', label: '安全设置', icon: Shield },
    { key: 'permissions', label: '权限管理', icon: Lock },
  ];

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">系统设置</h1>
        <p className="text-sm text-gray-500 mt-1">个性化配置您的运营平台</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="bg-white rounded-xl p-3 border border-gray-100 shadow-sm h-fit">
          <nav className="space-y-1">
            {tabs.map(({ key, label, icon: Icon }) => (
              <button
                key={key}
                onClick={() => setActiveTab(key)}
                className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors ${
                  activeTab === key
                    ? 'bg-blue-50 text-blue-700 font-medium'
                    : 'text-gray-600 hover:bg-gray-50'
                }`}
              >
                <Icon size={15} />
                {label}
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="lg:col-span-3 bg-white rounded-xl p-6 border border-gray-100 shadow-sm">
          {activeTab === 'account' && (
            <div className="space-y-6">
              <h3 className="font-semibold text-gray-900">账号偏好配置</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 block mb-2">平台偏好（主力运营平台）</label>
                  <div className="flex flex-wrap gap-2">
                    {['抖音', '小红书', '公众号', '视频号', 'B站', '快手'].map(p => (
                      <label key={p} className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                        <input type="checkbox" defaultChecked={['抖音', '小红书', '公众号'].includes(p)} className="accent-blue-600" />
                        <span className="text-sm text-gray-700">{p}</span>
                      </label>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700 block mb-2">内容风格偏好</label>
                  <select className="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    <option>专业干货型</option>
                    <option>轻松幽默型</option>
                    <option>情感共鸣型</option>
                    <option>种草安利型</option>
                  </select>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700 block mb-2">运营目标</label>
                  <div className="flex gap-3">
                    {['涨粉', '曝光', '变现', '品牌建设'].map(goal => (
                      <label key={goal} className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                        <input type="radio" name="goal" className="accent-blue-600" defaultChecked={goal === '涨粉'} />
                        <span className="text-sm text-gray-700">{goal}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="space-y-6">
              <h3 className="font-semibold text-gray-900">通知配置</h3>
              <div className="space-y-4">
                {[
                  { label: '数据异常预警', desc: '当核心数据偏差超过阈值时通知', checked: true },
                  { label: '内容发布提醒', desc: '发布计划执行前30分钟提醒', checked: true },
                  { label: '粉丝增长播报', desc: '每日粉丝增长数据播报', checked: false },
                  { label: '商单机会推送', desc: '有新的商单匹配时通知', checked: true },
                  { label: '周报生成通知', desc: '每周报告生成后通知', checked: true },
                ].map(item => (
                  <div key={item.label} className="flex items-center justify-between py-3 border-b border-gray-50 last:border-0">
                    <div>
                      <div className="text-sm font-medium text-gray-900">{item.label}</div>
                      <div className="text-xs text-gray-500 mt-0.5">{item.desc}</div>
                    </div>
                    <div className={`w-10 h-6 rounded-full relative cursor-pointer transition-colors ${item.checked ? 'bg-blue-500' : 'bg-gray-200'}`}>
                      <div className={`absolute top-1 w-4 h-4 bg-white rounded-full shadow transition-all ${item.checked ? 'left-5' : 'left-1'}`}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="space-y-6">
              <h3 className="font-semibold text-gray-900">界面个性化</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-sm font-medium text-gray-700 block mb-3">主题颜色</label>
                  <div className="flex gap-3">
                    {['#3B82F6', '#8B5CF6', '#10B981', '#F59E0B', '#EF4444', '#EC4899'].map(color => (
                      <button
                        key={color}
                        className={`w-8 h-8 rounded-full border-2 ${color === '#3B82F6' ? 'border-gray-400' : 'border-transparent'}`}
                        style={{ backgroundColor: color }}
                      />
                    ))}
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700 block mb-2">侧边栏样式</label>
                  <div className="flex gap-3">
                    {['深色（当前）', '浅色', '跟随系统'].map(style => (
                      <label key={style} className="flex items-center gap-2 px-3 py-2 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50">
                        <input type="radio" name="sidebar" className="accent-blue-600" defaultChecked={style === '深色（当前）'} />
                        <span className="text-sm text-gray-700">{style}</span>
                      </label>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {(activeTab === 'security' || activeTab === 'permissions') && (
            <div className="space-y-4">
              <h3 className="font-semibold text-gray-900">
                {activeTab === 'security' ? '安全设置' : '权限管理'}
              </h3>
              <div className="text-sm text-gray-500">此功能正在开发中，敬请期待...</div>
            </div>
          )}

          <div className="mt-6 pt-4 border-t border-gray-100 flex justify-end">
            <button className="flex items-center gap-2 px-5 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors">
              <Save size={14} />
              保存设置
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
