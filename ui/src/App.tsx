import { BrowserRouter, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import ContentTopics from './pages/ContentTopics';
import ContentGeneration from './pages/ContentGeneration';
import UserProfiles from './pages/UserProfiles';
import UserInteraction from './pages/UserInteraction';
import AnalyticsDashboard from './pages/AnalyticsDashboard';
import Distribution from './pages/Distribution';
import Monetization from './pages/Monetization';
import Monitor from './pages/Monitor';
import AISupport from './pages/AISupport';
import Settings from './pages/Settings';
import PlaceholderPage from './pages/PlaceholderPage';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Dashboard />} />

          {/* Content & Topics */}
          <Route path="content/topics" element={<ContentTopics />} />
          <Route path="content/generation" element={<ContentGeneration />} />
          <Route path="content/positioning" element={<PlaceholderPage title="账号定位与选题方向" desc="分析账号定位，智能规划选题方向，诊断账号健康度" />} />
          <Route path="content/planning" element={<PlaceholderPage title="内容创作规划" desc="内容排期生成，全流程创作支撑，内容矩阵规划" />} />
          <Route path="content/materials" element={<PlaceholderPage title="灵感与素材管理" desc="灵感捕捉，AI素材分类，素材库管理" />} />

          {/* User profiles & interaction */}
          <Route path="users/profiles" element={<UserProfiles />} />
          <Route path="users/interaction" element={<UserInteraction />} />
          <Route path="users/reach" element={<PlaceholderPage title="用户触达方案" desc="多渠道触达管理，个性化触达内容生成，效果追踪" />} />
          <Route path="users/private" element={<PlaceholderPage title="私域流量沉淀" desc="引流话术生成，私域工具对接，私域内容推荐" />} />

          {/* Analytics */}
          <Route path="analytics/dashboard" element={<AnalyticsDashboard />} />
          <Route path="analytics/insights" element={<PlaceholderPage title="智能数据分析" desc="内容效果归因，用户行为路径分析，数据预测" />} />
          <Route path="analytics/decisions" element={<PlaceholderPage title="决策辅助系统" desc="数据洞察报告，A/B测试工具，运营行动清单" />} />

          {/* Distribution */}
          <Route path="distribution" element={<Distribution />} />
          <Route path="distribution/adapt" element={<PlaceholderPage title="多平台内容适配" desc="智能格式转换，平台规则适配，多版本内容管理" />} />
          <Route path="distribution/schedule" element={<Distribution />} />
          <Route path="distribution/ads" element={<PlaceholderPage title="流量投放辅助" desc="预算智能分配，投放策略推荐，效果监控与优化" />} />

          {/* Monetization */}
          <Route path="monetization" element={<Monetization />} />
          <Route path="monetization/orders" element={<Monetization />} />
          <Route path="monetization/content" element={<PlaceholderPage title="内容变现" desc="知识付费支撑，电商带货，直播变现管理" />} />
          <Route path="monetization/private" element={<PlaceholderPage title="私域变现分析" desc="私域变现工具对接，变现效果分析，数据监控" />} />

          {/* Other modules */}
          <Route path="monitor" element={<Monitor />} />
          <Route path="ai-support" element={<AISupport />} />
          <Route path="workflow" element={<PlaceholderPage title="自动化工作流" desc="自定义自动化规则，第三方工具对接，流程自动化" />} />
          <Route path="security" element={<PlaceholderPage title="账号内容安全" desc="账号健康监控，内容合规检测，安全预警" />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
