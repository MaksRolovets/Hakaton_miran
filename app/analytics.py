import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import json

# Ваши данные (предположим, что они в переменной `data`)
data = {
  "title": "Форма3.Чек-лист оценки состояния (Помещение централизованной подачи материалов)",
  "classes": [
    {
      "letter": "A",
      "name": "Состояние рабочего пространства подсобного рабочего",
      "includeInScore": True,
      "questions": [
        {
          "id": "q-1-a1b2c3d4",
          "number": "1",
          "criterion": "На полу пыль, грязь. Под оборудованием и вокруг него отсутствует россыпи сырья, мусор, пакеты из-под материала, другие предметы",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-2-e5f6g7h8",
          "number": "2",
          "criterion": "Личные вещи отсутствуют в рабочей зоне работника (на оборудовании, стуле, стойке и т.д.), в том числе спецодежда",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-3-i9j0k1l2",
          "number": "3",
          "criterion": "На оборудовании и в рабочей зоне отсутствуют посторонние предметы, непредназначенные для выполнения профессиональных обязанностей",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-4-m3n4o5p6",
          "number": "4",
          "criterion": "Отсутствие пыли и грязи на оборудовании. Пол около оборудования чистый и сухой, нет разливов масла и других жидкостей",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-5-q7r8s9t0",
          "number": "5",
          "criterion": "Защитные стекла на оборудовании чистые",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-6-u1v2w3x4",
          "number": "6",
          "criterion": "Внутри оборудования отсутствуют посторонние предметы, в том числе остатки продукции от прошлых производственных партий",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        }
      ],
      "subclasses": []
    },
    {
      "letter": "B",
      "name": "Состояние оборудования",
      "includeInScore": True,
      "questions": [],
      "subclasses": [
        {
          "code": "B1",
          "name": "Ответственность персонала ЭМО",
          "includeInScore": True,
          "questions": [
            {
              "id": "q-1-y5z6a7b8",
              "number": "1",
              "criterion": "Течь масла, охлаждающих жидкостей с оборудования отсутствует. Пол около оборудования чистый и сухой",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Соответствует",
              "userComment": "",
              "userPhoto": None,
              "status": "Заполнено"
            },
            {
              "id": "q-2-c9d0e1f2",
              "number": "2",
              "criterion": "Внутри оборудования все элементы (провода, шланги и др.) закреплены монтажными стяжками. Все элементы оборудования закреплены резьбовыми соединениями (винтами, болтами, саморезами, гайками) и другими соединениями. Провода, шланги вокруг оборудования закреплены, не выступают в рабочую зону и не препятствуют безопасному перемещению внутри рабочей зоны",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Соответствует",
              "userComment": "",
              "userPhoto": None,
              "status": "Заполнено"
            },
            {
              "id": "q-3-g3h4i5j6",
              "number": "3",
              "criterion": "На оборудовании и других коммуникациях помещения отсутствуют повреждения изоляции электропроводки, лакокрасочных покрытий и т.д.",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Не соответствует",
              "userPhoto": "FILE:20260130_154258_q-3-g3h4i5j6.jpg",
              "userComment": "Отсутствует маркировка.",
              "status": "Заполнено"
            },
            {
              "id": "q-4-k7l8m9n0",
              "number": "4",
              "criterion": "Отсутствуют вещи, оставшиеся после работы вспомогательных служб на производственном участке",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Соответствует",
              "userComment": "",
              "userPhoto": None,
              "status": "Заполнено"
            },
            {
              "id": "q-5-o1p2q3r4",
              "number": "5",
              "criterion": "Панель управления в технически исправном состоянии, все надписи читаемы, видимые повреждения отсутствуют",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Соответствует",
              "userComment": "",
              "userPhoto": None,
              "status": "Заполнено"
            },
            {
              "id": "q-6-s5t6u7v8",
              "number": "6",
              "criterion": "На оборудовании имеются все защитные ограждения, предусмотренные конструкцией оборудования, в том числе закрывающие подвижные механизмы. Защитные стекла целые, не имеют трещин и сколов",
              "defaultValue": "Соответствует",
              "allowGallery": True,
              "allowPhoto": True,
              "includeInScore": True,
              "userAnswer": "Соответствует",
              "userComment": "",
              "userPhoto": None,
              "status": "Заполнено"
            }
          ]
        }
      ]
    },
    {
      "letter": "C",
      "name": "Состояние помещения",
      "includeInScore": True,
      "questions": [
        {
          "id": "q-1-w9x0y1z2",
          "number": "1",
          "criterion": "Пол, подоконники, колонны, стены, двери чистые (нет пыли, грязи и др.) и не имеют повреждений",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-2-a3b4c5d6",
          "number": "2",
          "criterion": "Уборочный инвентарь размещен аккуратно в установленном месте, в необходимом количестве и ассортименте",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-3-e7f8g9h0",
          "number": "3",
          "criterion": "Все отходы собираются раздельно. Контейнеры размещены в установленном месте, идентифицированы и используются по назначению",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-4-i1j2k3l4",
          "number": "4",
          "criterion": "Места, предназначенные для хранения сырья, основных и вспомогательных материалов, тележек, поддонов идентифицированы и в исправном состоянии. В местах хранения размещены предметы, соответствующие идентификационным надписям",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-5-m5n6o7p8",
          "number": "5",
          "criterion": "Проходы и проезды без загромождений материалами, сырьем, поддонами, посторонними предметами и др.ТМЦ, все предметы размещены в установленных местах, имеющих соответствующую цветовую разметку",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        },
        {
          "id": "q-6-q9r0s1t2",
          "number": "6",
          "criterion": "Электроштабелеры, гидротележеки размещены в установленных местах, идентифицированы наименованием участка и имеют отметку о последних испытаниях",
          "defaultValue": "Соответствует",
          "allowGallery": True,
          "allowPhoto": True,
          "includeInScore": True,
          "userAnswer": "Соответствует",
          "userComment": "",
          "userPhoto": None,
          "status": "Заполнено"
        }
      ],
      "subclasses": []
    }
  ],
  "department": "Отделение раздува",
  "completionDate": "2026-01-30T15:42:41.972006"
}

def flatten_checklist_data(data):
    """Преобразует иерархические данные чек-листа в плоский DataFrame."""
    rows = []
    
    for class_obj in data['classes']:
        # Обрабатываем вопросы основного класса
        for question in class_obj.get('questions', []):
            rows.append({
                'class_letter': class_obj['letter'],
                'class_name': class_obj['name'],
                'subclass_code': None,
                'subclass_name': None,
                'question_id': question['id'],
                'question_number': question['number'],
                'criterion': question['criterion'],
                'user_answer': question['userAnswer'],
                'user_comment': question['userComment'],
                'has_photo': question['userPhoto'] is not None,
                'include_in_score': question['includeInScore']
            })
        
        # Обрабатываем подклассы
        for subclass in class_obj.get('subclasses', []):
            for question in subclass.get('questions', []):
                rows.append({
                    'class_letter': class_obj['letter'],
                    'class_name': class_obj['name'],
                    'subclass_code': subclass.get('code'),
                    'subclass_name': subclass.get('name'),
                    'question_id': question['id'],
                    'question_number': question['number'],
                    'criterion': question['criterion'],
                    'user_answer': question['userAnswer'],
                    'user_comment': question['userComment'],
                    'has_photo': question['userPhoto'] is not None,
                    'include_in_score': question['includeInScore']
                })
    
    return pd.DataFrame(rows)

# Создаем DataFrame
df = flatten_checklist_data(data)
print(f"Всего записей: {len(df)}")
print(f"Уникальных проверок: {df['question_id'].nunique()}")

def get_top_violations(df, top_n=10):
    """Анализирует и возвращает топ нарушений."""
    # Фильтруем только несоответствия
    violations = df[df['user_answer'] == 'Не соответствует'].copy()
    
    if violations.empty:
        print("Нарушений не обнаружено!")
        return None
    
    # Группируем по критериям
    violation_stats = violations.groupby(['class_name', 'criterion']).agg({
        'question_id': 'count',
        'has_photo': 'sum',
        'user_comment': lambda x: x[x != ""].count()  # Кол-во непустых комментариев
    }).rename(columns={
        'question_id': 'count',
        'has_photo': 'photos_count',
        'user_comment': 'comments_count'
    }).reset_index()
    
    # Сортируем по количеству нарушений
    violation_stats = violation_stats.sort_values('count', ascending=False).head(top_n)
    
    return violation_stats

# Визуализация топ нарушений
def plot_top_violations(violation_stats, top_n=10):
    """Строит график топ нарушений."""
    plt.figure(figsize=(12, 8))
    
    # Создаем комбинированные labels для лучшей читаемости
    labels = [f"{row['class_name']}\n{row['criterion'][:80]}..." 
              for _, row in violation_stats.head(top_n).iterrows()]
    
    bars = plt.barh(range(len(labels)), violation_stats.head(top_n)['count'])
    plt.yticks(range(len(labels)), labels)
    plt.xlabel('Количество нарушений')
    plt.title(f'Топ-{top_n} нарушений')
    plt.gca().invert_yaxis()
    
    # Добавляем аннотации с количеством
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2, 
                f"{int(bar.get_width())}", ha='left', va='center')
    
    plt.tight_layout()
    plt.show()

# Анализ
violation_stats = get_top_violations(df)
if violation_stats is not None:
    print("Топ нарушений:")
    print(violation_stats[['class_name', 'criterion', 'count']].head())
    plot_top_violations(violation_stats)


def create_compliance_heatmap(df):
    """Создает тепловую карту уровня соответствия по классам/подклассам."""
    
    # Вычисляем процент соответствия для каждой группы
    def calculate_compliance(group):
        total = len(group)
        compliant = len(group[group['user_answer'] == 'Соответствует'])
        return (compliant / total) * 100 if total > 0 else 0
    
    # Группируем по классам и подклассам
    if 'subclass_code' in df.columns and df['subclass_code'].notna().any():
        # Если есть подклассы
        compliance_data = df.groupby(['class_name', 'subclass_name']).apply(calculate_compliance).unstack()
    else:
        # Только по классам
        compliance_data = df.groupby('class_name').apply(calculate_compliance).to_frame('compliance_rate')
        compliance_data = compliance_data.T  # Транспонируем для heatmap
    
    # Визуализация
    plt.figure(figsize=(12, 8))
    sns.heatmap(compliance_data, 
                annot=True, 
                fmt='.1f', 
                cmap='RdYlGn',
                vmin=0, 
                vmax=100,
                cbar_kws={'label': 'Процент соответствия, %'})
    plt.title('Тепловая карта соответствия требованиям')
    plt.tight_layout()
    plt.show()
    
    return compliance_data

# Создаем тепловую карту
compliance_heatmap = create_compliance_heatmap(df)

class EmployeeKPI:
    """Класс для расчета KPI сотрудников на основе данных чек-листов."""
    
    def __init__(self, df):
        self.df = df
        self.results = {}
    
    def calculate_department_kpi(self, department_name):
        """Расчет KPI для отдела/участка."""
        
        # Базовые метрики
        total_checks = len(self.df)
        compliant_checks = len(self.df[self.df['user_answer'] == 'Соответствует'])
        non_compliant_checks = len(self.df[self.df['user_answer'] == 'Не соответствует'])
        
        # Основной KPI - процент соответствия
        compliance_rate = (compliant_checks / total_checks) * 100 if total_checks > 0 else 0
        
        # Дополнительные метрики
        checks_with_photos = self.df['has_photo'].sum()
        checks_with_comments = self.df[self.df['user_comment'] != ""].shape[0]
        
        # Вес нарушений (можно настроить)
        critical_violations = len(self.df[
            (self.df['user_answer'] == 'Не соответствует') & 
            (self.df['class_letter'].isin(['B']))  # Нарушения в оборудовании - критические
        ])
        
        kpi_score = max(0, compliance_rate - (critical_violations * 5))
        
        return {
            'department': department_name,
            'total_checks': total_checks,
            'compliance_rate': compliance_rate,
            'non_compliant_count': non_compliant_checks,
            'critical_violations': critical_violations,
            'documentation_quality': (checks_with_photos + checks_with_comments) / total_checks * 50,
            'kpi_score': kpi_score,
            'rating': self._get_rating(kpi_score)
        }
    
    def _get_rating(self, score):
        """Определяет рейтинг на основе KPI."""
        if score >= 95: return "Отлично"
        elif score >= 85: return "Хорошо"
        elif score >= 70: return "Удовлетворительно"
        else: return "Требует улучшения"
    
    def generate_kpi_report(self, department_name):
        """Генерирует полный отчет KPI."""
        kpi = self.calculate_department_kpi(department_name)
        
        print(f"=== KPI ОТЧЕТ: {department_name} ===")
        print(f"Общее количество проверок: {kpi['total_checks']}")
        print(f"Процент соответствия: {kpi['compliance_rate']:.1f}%")
        print(f"Количество несоответствий: {kpi['non_compliant_count']}")
        print(f"Критические нарушения: {kpi['critical_violations']}")
        print(f"Качество документации: {kpi['documentation_quality']:.1f}%")
        print(f"Итоговый KPI: {kpi['kpi_score']:.1f}")
        print(f"Рейтинг: {kpi['rating']}")
        
        return kpi

# Использование
kpi_calculator = EmployeeKPI(df)
kpi_report = kpi_calculator.generate_kpi_report(data['department'])

def comprehensive_analysis(df, data):
    """Комплексный анализ данных чек-листа."""
    
    print("=== КОМПЛЕКСНЫЙ АНАЛИЗ ЧЕК-ЛИСТА ===")
    
    # Общая статистика
    total_questions = len(df)
    compliance_rate = (len(df[df['user_answer'] == 'Соответствует']) / total_questions) * 100
    violation_rate = 100 - compliance_rate
    
    print(f"Дата проверки: {data['completionDate']}")
    print(f"Отделение: {data['department']}")
    print(f"Общее количество пунктов: {total_questions}")
    print(f"Общий процент соответствия: {compliance_rate:.1f}%")
    print(f"Общий процент нарушений: {violation_rate:.1f}%")
    
    # Анализ по классам
    print("\n--- Анализ по разделам ---")
    class_stats = df.groupby('class_name').agg({
        'user_answer': lambda x: (x == 'Соответствует').sum() / len(x) * 100,
        'question_id': 'count'
    }).rename(columns={'user_answer': 'compliance_%', 'question_id': 'total_checks'})
    
    print(class_stats)
    
    # Анализ документации
    photos_percentage = (df['has_photo'].sum() / len(df)) * 100
    comments_percentage = (df[df['user_comment'] != ""].shape[0] / len(df)) * 100
    
    print(f"\n--- Качество документации ---")
    print(f"Пунктов с фотографиями: {photos_percentage:.1f}%")
    print(f"Пунктов с комментариями: {comments_percentage:.1f}%")
    
    return {
        'total_compliance': compliance_rate,
        'class_stats': class_stats,
        'photos_percentage': photos_percentage,
        'comments_percentage': comments_percentage
    }

# Запуск комплексного анализа
analysis_results = comprehensive_analysis(df, data)

def plot_answer_distribution(df):
    """Визуализация распределения ответов."""
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Круговая диаграмма общего распределения
    answer_counts = df['user_answer'].value_counts()
    axes[0].pie(answer_counts.values, labels=answer_counts.index, autopct='%1.1f%%')
    axes[0].set_title('Общее распределение ответов')
    
    # Столбчатая диаграмма по классам
    compliance_by_class = df.groupby(['class_name', 'user_answer']).size().unstack(fill_value=0)
    compliance_by_class.plot(kind='bar', ax=axes[1], stacked=True)
    axes[1].set_title('Распределение ответов по разделам')
    axes[1].set_ylabel('Количество пунктов')
    axes[1].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()

plot_answer_distribution(df)