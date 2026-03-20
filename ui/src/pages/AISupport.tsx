import { Bot, Zap, Settings2, CheckCircle2, ArrowRight, Cpu, Brain, Wand2 } from 'lucide-react';

const models = [
  { name: 'GPT-4o', provider: 'OpenAI', status: 'active', tasks: ['内容生成', '选题分析', '数据解读'], speed: '快', quality: '最高' },
  { name: 'Claude 3.5 Sonnet', provider: 'Anthropic', status: 'active', tasks: ['长文创作', '代码生成'], speed: '快', quality: '很高' },
  { name: '文心一言4.0', provider: '百度', status: 'standby', tasks: ['中文创作', '内容审核'], speed: '中', quality: '高' },
  { name: '通义千问Plus', provider: '阿里云', status: 'standby', tasks: ['数据分析', '报告生成'], speed: '快', quality: '高' },
];

const workflows = [
  { name: '粉丝新增触发欢迎私信', trigger: '粉丝新增≥100', action: '发送欢迎私信模板', status: 'active', runs: 128 },
  { name: '爆款内容触发复盘报告', trigger: '互动量超过均值200%', action: '生成内容复盘报告', status: 'active', runs: 23 },
  { name: '每周自动生成选题日历', trigger: '每周日 22:00', action: '生成下周选题建议', status: 'active', runs: 12 },
  { name: '数据异常预警通知', trigger: '核心指标偏差>20%', action: '发送预警通知', status: 'active', runs: 45 },
];

export default function AISupport() {
  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">AI技术支撑</h1>
        <p className="text-sm text-gray-500 mt-1">多模型协同工作，全流程AI赋能</p>
      </div>

      {/* AI stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {[
          { label: '今日AI生成任务', value: '127', icon: Brain, color: 'bg-blue-500' },
          { label: '内容生成耗时均值', value: '2.3min', icon: Zap, color: 'bg-purple-500' },
          { label: '提示词模板数', value: '143', icon: Wand2, color: 'bg-orange-500' },
          { label: 'AI准确率', value: '94.2%', icon: CheckCircle2, color: 'bg-green-500' },
        ].map(stat => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="bg-white rounded-xl p-4 border border-gray-100 shadow-sm">
              <div className="flex items-center justify-between mb-2">
                <div className={`w-9 h-9 ${stat.color} rounded-lg flex items-center justify-center`}>
                  <Icon size={16} className="text-white" />
                </div>
              </div>
              <div className="text-xl font-bold text-gray-900">{stat.value}</div>
              <div className="text-xs text-gray-500 mt-0.5">{stat.label}</div>
            </div>
          );
        })}
      </div>

      {/* Models */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Cpu size={16} className="text-blue-500" />
          接入模型管理
        </h3>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {models.map(model => (
            <div key={model.name} className={`p-4 rounded-xl border ${model.status === 'active' ? 'border-blue-200 bg-blue-50' : 'border-gray-100 bg-gray-50'}`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Bot size={16} className={model.status === 'active' ? 'text-blue-600' : 'text-gray-400'} />
                  <span className="font-medium text-sm text-gray-900">{model.name}</span>
                </div>
                <span className={`text-xs px-2 py-0.5 rounded-full ${model.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                  {model.status === 'active' ? '运行中' : '备用'}
                </span>
              </div>
              <p className="text-xs text-gray-500 mb-2">{model.provider}</p>
              <div className="flex flex-wrap gap-1.5">
                {model.tasks.map(task => (
                  <span key={task} className="px-2 py-0.5 bg-white text-gray-600 text-xs rounded-full border border-gray-200">{task}</span>
                ))}
              </div>
              <div className="flex gap-4 mt-3 text-xs text-gray-500">
                <span>速度: <strong className="text-gray-700">{model.speed}</strong></span>
                <span>质量: <strong className="text-gray-700">{model.quality}</strong></span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Automation workflows */}
      <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
        <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
          <Settings2 size={16} className="text-purple-500" />
          自动化工作流
        </h3>
        <div className="space-y-3">
          {workflows.map((wf, i) => (
            <div key={i} className="flex items-center gap-4 p-4 border border-gray-100 rounded-xl hover:border-gray-200 transition-colors">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm font-medium text-gray-900">{wf.name}</span>
                  <span className={`text-xs px-2 py-0.5 rounded-full ${wf.status === 'active' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'}`}>
                    {wf.status === 'active' ? '运行中' : '已停止'}
                  </span>
                </div>
                <div className="flex items-center gap-2 text-xs text-gray-500">
                  <span className="bg-yellow-50 text-yellow-700 px-2 py-0.5 rounded">触发: {wf.trigger}</span>
                  <ArrowRight size={12} />
                  <span className="bg-blue-50 text-blue-700 px-2 py-0.5 rounded">动作: {wf.action}</span>
                </div>
              </div>
              <div className="text-xs text-gray-400 text-right flex-shrink-0">
                <div className="font-medium text-gray-700">{wf.runs}次</div>
                <div>已执行</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
