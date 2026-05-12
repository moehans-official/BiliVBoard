import asyncio
import sys
from collector.utils import load_bvids
from collector.data_collector import collect_all_data
from collector.excel_handler import create_excel_report


def select_formula():
    """交互式选择评分公式"""
    print('\n请选择评分公式:')
    print('1. V3 Normal (普通版) - 半衰期约20.79天')
    print('2. V3 Radical (激进版) - 半衰期约6.93天')
    print('3. V3 E SP (事件激增版) - 需要额外数据')
    
    while True:
        choice = input('\n请输入选择 (1/2/3，默认1): ').strip()
        if choice == '' or choice == '1':
            return 'normal'
        elif choice == '2':
            return 'radical'
        elif choice == '3':
            return 'e_sp'
        else:
            print('无效选择，请输入1、2或3')


async def main():
    # 从命令行参数获取公式，或交互式选择
    if len(sys.argv) > 1:
        formula = sys.argv[1]
        if formula not in ['normal', 'radical', 'e_sp']:
            print(f'无效公式: {formula}，使用默认公式 normal')
            formula = 'normal'
    else:
        formula = select_formula()
    
    print(f'使用公式: {formula}')
    
    bvids = load_bvids()
    if not bvids:
        print('bvid.txt 中没有有效的 BV 号')
        return
    
    results = await collect_all_data(bvids, formula)
    output_file = create_excel_report(results)
    print(f'已保存至 {output_file}，共处理 {len(results)} 个视频')


if __name__ == '__main__':
    asyncio.run(main())
