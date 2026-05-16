import { useState } from 'react';
import { NavLink, Outlet } from 'react-router-dom';
import {
  LayoutDashboard,
  Lightbulb,
  Users,
  BarChart2,
  Share2,
  DollarSign,
  Settings,
  Bell,
  Search,
  ChevronDown,
  Menu,
  X,
  Bot,
  Shield,
  Workflow,
  Activity,
  ChevronRight,
} from 'lucide-react';

const navItems = [
  {
    label: '数据概览',
    icon: LayoutDashboard,
    path: '/',
  },
  {
    label: '智能选题与内容生成',
    icon: Lightbulb,
    path: '/content',
    children: [
      { label: '账号定位与选题', path: '/content/positioning' },
      { label: '智能选题引擎', path: '/content/topics' },
      { label: '内容创作规划', path: '/content/planning' },
      { label: '多模态内容生成', path: '/content/generation' },
      { label: '素材管理', path: '/content/materials' },
    ],
  },
  {
    label: '用户画像与精准互动',
    icon: Users,
    path: '/users',
    children: [
      { label: '用户画像构建', path: '/users/profiles' },
      { label: '用户触达方案', path: '/users/reach' },
      { label: '智能互动系统', path: '/users/interaction' },
      { label: '私域流量沉淀', path: '/users/private' },
    ],
  },
  {
    label: '数据检测与智能决策',
    icon: BarChart2,
    path: '/analytics',
    children: [
      { label: '实时数据看板', path: '/analytics/dashboard' },
      { label: '智能数据分析', path: '/analytics/insights' },
      { label: '决策辅助系统', path: '/analytics/decisions' },
    ],
  },
  {
    label: '跨平台智能分发',
    icon: Share2,
    path: '/distribution',
    children: [
      { label: '多平台内容适配', path: '/distribution/adapt' },
      { label: '智能发布调度', path: '/distribution/schedule' },
      { label: '流量投放辅助', path: '/distribution/ads' },
    ],
  },
  {
    label: '商业变现赋能',
    icon: DollarSign,
    path: '/monetization',
    children: [
      { label: '商单匹配系统', path: '/monetization/orders' },
      { label: '内容变现', path: '/monetization/content' },
      { label: '私域变现分析', path: '/monetization/private' },
    ],
  },
  {
    label: '运营监控',
    icon: Activity,
    path: '/monitor',
  },
  {
    label: 'AI技术支撑',
    icon: Bot,
    path: '/ai-support',
  },
  {
    label: '自动化工作流',
    icon: Workflow,
    path: '/workflow',
  },
  {
    label: '账号内容安全',
    icon: Shield,
    path: '/security',
  },
  {
    label: '系统设置',
    icon: Settings,
    path: '/settings',
  },
];

export default function MainLayout() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [expandedItems, setExpandedItems] = useState<string[]>(['/content', '/users', '/analytics', '/distribution', '/monetization']);

  const toggleExpand = (path: string) => {
    setExpandedItems(prev =>
      prev.includes(path) ? prev.filter(p => p !== path) : [...prev, path]
    );
  };

  return (
    <div className="flex h-screen bg-gray-50 font-sans">
      {/* Sidebar */}
      <aside
        className={`${sidebarOpen ? 'w-64' : 'w-0 overflow-hidden'} bg-slate-900 text-white flex flex-col transition-all duration-300 ease-in-out flex-shrink-0`}
      >
        {/* Logo */}
        <div className="flex items-center gap-3 px-5 py-4 border-b border-slate-700">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-400 to-purple-600 rounded-lg flex items-center justify-center">
            <Bot size={18} className="text-white" />
          </div>
          <div>
            <div className="font-bold text-sm text-white leading-tight">AI智能自媒体</div>
            <div className="text-xs text-slate-400 leading-tight">运营平台</div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 overflow-y-auto py-4 px-2 space-y-0.5">
          {navItems.map(item => {
            const Icon = item.icon;
            const hasChildren = item.children && item.children.length > 0;
            const isExpanded = expandedItems.includes(item.path);

            return (
              <div key={item.path}>
                {hasChildren ? (
                  <button
                    onClick={() => toggleExpand(item.path)}
                    className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-slate-300 hover:bg-slate-800 hover:text-white transition-colors text-sm"
                  >
                    <Icon size={16} />
                    <span className="flex-1 text-left truncate">{item.label}</span>
                    {isExpanded ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
                  </button>
                ) : (
                  <NavLink
                    to={item.path}
                    end={item.path === '/'}
                    className={({ isActive }) =>
                      `flex items-center gap-3 px-3 py-2 rounded-lg text-sm transition-colors ${
                        isActive
                          ? 'bg-blue-600 text-white'
                          : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                      }`
                    }
                  >
                    <Icon size={16} />
                    <span className="truncate">{item.label}</span>
                  </NavLink>
                )}

                {/* Children */}
                {hasChildren && isExpanded && (
                  <div className="ml-4 mt-0.5 space-y-0.5 border-l border-slate-700 pl-3">
                    {item.children!.map(child => (
                      <NavLink
                        key={child.path}
                        to={child.path}
                        className={({ isActive }) =>
                          `flex items-center gap-2 px-2 py-1.5 rounded-lg text-xs transition-colors ${
                            isActive
                              ? 'bg-blue-600 text-white'
                              : 'text-slate-400 hover:bg-slate-800 hover:text-white'
                          }`
                        }
                      >
                        <span className="truncate">{child.label}</span>
                      </NavLink>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>

        {/* User info at bottom */}
        <div className="border-t border-slate-700 px-4 py-3 flex items-center gap-3">
          <div className="w-8 h-8 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center text-xs font-bold">
            管
          </div>
          <div className="flex-1 min-w-0">
            <div className="text-sm text-white font-medium truncate">管理员</div>
            <div className="text-xs text-slate-400 truncate">admin@ai-wemedia.com</div>
          </div>
        </div>
      </aside>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <header className="bg-white border-b border-gray-200 px-4 py-3 flex items-center gap-4 flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(prev => !prev)}
            className="text-gray-500 hover:text-gray-700 transition-colors"
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          {/* Search */}
          <div className="flex-1 max-w-md">
            <div className="relative">
              <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
              <input
                type="text"
                placeholder="搜索功能、数据、内容..."
                className="w-full pl-9 pr-4 py-2 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

          <div className="flex items-center gap-3 ml-auto">
            {/* Notifications */}
            <button className="relative text-gray-500 hover:text-gray-700 p-2 rounded-lg hover:bg-gray-100 transition-colors">
              <Bell size={18} />
              <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>

            {/* User menu */}
            <button className="flex items-center gap-2 text-sm text-gray-700 hover:text-gray-900 px-3 py-2 rounded-lg hover:bg-gray-100 transition-colors">
              <div className="w-7 h-7 bg-gradient-to-br from-green-400 to-blue-500 rounded-full flex items-center justify-center text-xs font-bold text-white">
                管
              </div>
              <span className="font-medium">管理员</span>
              <ChevronDown size={14} className="text-gray-400" />
            </button>
          </div>
        </header>

        {/* Page content */}
        <main className="flex-1 overflow-y-auto">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
