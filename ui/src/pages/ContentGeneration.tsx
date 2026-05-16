import { useState } from 'react';
import {
  FileText, Image, Video, Music, Wand2, Copy, Download,
  CheckCircle2, Clock, RefreshCw, Settings2,
  Zap, ArrowRight, AlertTriangle
} from 'lucide-react';

const platforms = ['小红书', '抖音', '公众号', '视频号', 'B站'];
const styles = ['专业干货', '轻松幽默', '情感共鸣', '种草安利', '数据驱动'];
const wordCounts = ['500字', '800字', '1200字', '2000字', '自定义'];

const generatedContent = {
  title: '素人护肤博主必看！这6个平价护肤成分，让你少走10年弯路',
  body: `大家好，我是你们的护肤博主！

今天要给大家分享一个超级重要的护肤知识——那些真正有效的平价护肤成分！

💡 **成分一：烟酰胺**
控油、美白、收缩毛孔三合一！浓度建议2%-5%，敏感肌从低浓度开始用。推荐搭配保湿精华一起使用效果更佳。

💡 **成分二：玻尿酸（透明质酸）**
保湿神器！分子量越小渗透性越好，但敏感肌注意不要使用纯水+玻尿酸的组合，容易"吸水反干"。

💡 **成分三：维生素C（抗坏血酸）**
美白+抗氧化双重效果！浓度10%-20%效果最佳，建议早上使用配合防晒，注意避光保存。

💡 **成分四：A醇（视黄醇）**
抗衰老+改善痘印效果显著！新手从0.025%-0.05%低浓度入手，建议只在晚上使用。

💡 **成分五：水杨酸**
闭口粉刺专用！2%浓度溶解角质，疏通毛孔，干皮和敏感肌谨慎使用。

💡 **成分六：积雪草苷**
修复屏障的宝藏成分！舒缓泛红，修复受损皮肤屏障，敏感肌闭眼入！

❓ **哪些成分不能同时用？**
- 维C + A醇 = 不建议同时使用（刺激性叠加）
- 果酸/水杨酸 + A醇 = 同样要分开使用
- 烟酰胺 + 维C = 其实可以同时用（早已辟谣）

📌 **保存这篇攻略，护肤少踩坑！**

#护肤 #平价护肤 #成分党 #干货分享 #护肤攻略`,
  tags: ['#护肤', '#平价护肤', '#成分党', '#干货分享', '#护肤攻略'],
  originalityScore: 87,
  readabilityScore: 92,
  complianceScore: 98,
  valueScore: 90,
};

type ContentType = 'text' | 'image' | 'video' | 'audio';

export default function ContentGeneration() {
  const [selectedPlatform, setSelectedPlatform] = useState('小红书');
  const [selectedStyle, setSelectedStyle] = useState('专业干货');
  const [selectedWordCount, setSelectedWordCount] = useState('1200字');
  const [activeContentType, setActiveContentType] = useState<ContentType>('text');
  const [topic, setTopic] = useState('平价护肤成分解析，帮助敏感肌用户避坑');
  const [generating, setGenerating] = useState(false);
  const [generated, setGenerated] = useState(true);

  const contentTypes: { key: ContentType; icon: React.ElementType; label: string }[] = [
    { key: 'text', icon: FileText, label: '文本生成' },
    { key: 'image', icon: Image, label: '视觉生成' },
    { key: 'video', icon: Video, label: '视频脚本' },
    { key: 'audio', icon: Music, label: '配音文案' },
  ];

  const handleGenerate = () => {
    setGenerating(true);
    setTimeout(() => {
      setGenerating(false);
      setGenerated(true);
    }, 2000);
  };

  const getScoreColor = (score: number) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 75) return 'text-blue-600';
    return 'text-yellow-600';
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">多模态内容生成</h1>
        <p className="text-sm text-gray-500 mt-1">AI一键生成高质量内容，支持文本、图片、视频、音频多种形式</p>
      </div>

      {/* Content type tabs */}
      <div className="flex gap-3">
        {contentTypes.map(({ key, icon: Icon, label }) => (
          <button
            key={key}
            onClick={() => setActiveContentType(key)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl border text-sm font-medium transition-all ${
              activeContentType === key
                ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-100'
                : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
            }`}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Configuration panel */}
        <div className="lg:col-span-2 space-y-4">
          <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
            <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Settings2 size={16} />
              生成配置
            </h3>

            {/* Topic input */}
            <div className="space-y-4">
              <div>
                <label className="text-xs font-medium text-gray-700 mb-1.5 block">选题/主题</label>
                <textarea
                  value={topic}
                  onChange={(e) => setTopic(e.target.value)}
                  rows={3}
                  className="w-full text-sm border border-gray-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="输入选题或创作主题..."
                />
              </div>

              {/* Platform */}
              <div>
                <label className="text-xs font-medium text-gray-700 mb-1.5 block">目标平台</label>
                <div className="flex flex-wrap gap-2">
                  {platforms.map(p => (
                    <button
                      key={p}
                      onClick={() => setSelectedPlatform(p)}
                      className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                        selectedPlatform === p
                          ? 'bg-blue-600 text-white border-blue-600'
                          : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {p}
                    </button>
                  ))}
                </div>
              </div>

              {/* Style */}
              <div>
                <label className="text-xs font-medium text-gray-700 mb-1.5 block">内容风格</label>
                <div className="flex flex-wrap gap-2">
                  {styles.map(s => (
                    <button
                      key={s}
                      onClick={() => setSelectedStyle(s)}
                      className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                        selectedStyle === s
                          ? 'bg-purple-600 text-white border-purple-600'
                          : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {s}
                    </button>
                  ))}
                </div>
              </div>

              {/* Word count */}
              <div>
                <label className="text-xs font-medium text-gray-700 mb-1.5 block">字数设置</label>
                <div className="flex gap-2">
                  {wordCounts.map(w => (
                    <button
                      key={w}
                      onClick={() => setSelectedWordCount(w)}
                      className={`px-3 py-1 text-xs rounded-full border transition-colors ${
                        selectedWordCount === w
                          ? 'bg-green-600 text-white border-green-600'
                          : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
                      }`}
                    >
                      {w}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={generating}
              className="w-full mt-4 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium text-sm flex items-center justify-center gap-2 hover:opacity-90 transition-opacity disabled:opacity-70"
            >
              {generating ? (
                <>
                  <RefreshCw size={16} className="animate-spin" />
                  AI生成中...
                </>
              ) : (
                <>
                  <Wand2 size={16} />
                  一键AI生成
                </>
              )}
            </button>
          </div>

          {/* Quality scores */}
          {generated && (
            <div className="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
              <h3 className="font-semibold text-gray-900 mb-4 flex items-center gap-2">
                <CheckCircle2 size={16} className="text-green-500" />
                内容质量检测
              </h3>
              <div className="space-y-3">
                {[
                  { label: '原创度', score: generatedContent.originalityScore, icon: '✍️' },
                  { label: '可读性', score: generatedContent.readabilityScore, icon: '📖' },
                  { label: '合规性', score: generatedContent.complianceScore, icon: '✅' },
                  { label: '价值感', score: generatedContent.valueScore, icon: '💎' },
                ].map(item => (
                  <div key={item.label} className="flex items-center gap-3">
                    <span className="text-base w-6">{item.icon}</span>
                    <div className="flex-1">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-600">{item.label}</span>
                        <span className={`font-bold ${getScoreColor(item.score)}`}>{item.score}</span>
                      </div>
                      <div className="h-1.5 bg-gray-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full ${item.score >= 90 ? 'bg-green-500' : item.score >= 75 ? 'bg-blue-500' : 'bg-yellow-500'}`}
                          style={{ width: `${item.score}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              <div className="mt-3 p-2.5 bg-green-50 rounded-lg border border-green-100">
                <p className="text-xs text-green-700 flex items-center gap-1.5">
                  <CheckCircle2 size={12} />
                  内容质量优秀，可直接发布或做少量润色
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Generated content */}
        <div className="lg:col-span-3">
          {generated ? (
            <div className="bg-white rounded-xl border border-gray-100 shadow-sm overflow-hidden">
              {/* Content header */}
              <div className="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-md font-medium">{selectedPlatform}</span>
                  <span className="px-2 py-1 bg-purple-100 text-purple-700 text-xs rounded-md font-medium">{selectedStyle}</span>
                  <span className="text-xs text-gray-400 flex items-center gap-1">
                    <Clock size={11} />
                    刚刚生成
                  </span>
                </div>
                <div className="flex gap-2">
                  <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                    <Copy size={15} />
                  </button>
                  <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                    <Download size={15} />
                  </button>
                  <button className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors">
                    <RefreshCw size={15} />
                  </button>
                </div>
              </div>

              {/* Content body */}
              <div className="p-5 space-y-4">
                {/* Title */}
                <div>
                  <label className="text-xs font-medium text-gray-500 block mb-1">标题</label>
                  <div className="text-base font-bold text-gray-900 bg-yellow-50 p-3 rounded-lg border border-yellow-100">
                    {generatedContent.title}
                  </div>
                </div>

                {/* Body */}
                <div>
                  <label className="text-xs font-medium text-gray-500 block mb-1">正文</label>
                  <div className="text-sm text-gray-700 leading-relaxed bg-gray-50 p-4 rounded-lg border border-gray-100 max-h-96 overflow-y-auto whitespace-pre-line">
                    {generatedContent.body}
                  </div>
                </div>

                {/* Tags */}
                <div>
                  <label className="text-xs font-medium text-gray-500 block mb-1.5">话题标签</label>
                  <div className="flex flex-wrap gap-2">
                    {generatedContent.tags.map(tag => (
                      <span key={tag} className="px-2.5 py-1 bg-blue-50 text-blue-700 text-xs rounded-full border border-blue-100">
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action buttons */}
              <div className="px-5 py-4 border-t border-gray-100 flex gap-3">
                <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700 transition-colors font-medium">
                  <Zap size={14} />
                  直接发布
                </button>
                <button className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white text-sm rounded-lg hover:bg-green-700 transition-colors font-medium">
                  <Clock size={14} />
                  加入发布队列
                </button>
                <button className="flex items-center gap-2 px-4 py-2 border border-gray-200 text-gray-700 text-sm rounded-lg hover:bg-gray-50 transition-colors">
                  <ArrowRight size={14} />
                  多平台适配
                </button>
              </div>
            </div>
          ) : (
            <div className="bg-white rounded-xl border border-dashed border-gray-200 p-12 flex flex-col items-center justify-center text-center">
              <Wand2 size={40} className="text-gray-300 mb-4" />
              <h3 className="text-gray-500 font-medium">配置参数后点击"一键AI生成"</h3>
              <p className="text-sm text-gray-400 mt-2">AI将根据您的配置生成高质量内容</p>
            </div>
          )}

          {/* Compliance warning */}
          {generated && (
            <div className="mt-3 bg-yellow-50 rounded-xl p-4 border border-yellow-100 flex items-start gap-3">
              <AlertTriangle size={16} className="text-yellow-600 mt-0.5 flex-shrink-0" />
              <div>
                <p className="text-sm font-medium text-yellow-800">合规提示</p>
                <p className="text-xs text-yellow-700 mt-0.5">内容已通过敏感词检测和原创度检验（87%），建议发布前确认商品数据的真实性与准确性。</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
