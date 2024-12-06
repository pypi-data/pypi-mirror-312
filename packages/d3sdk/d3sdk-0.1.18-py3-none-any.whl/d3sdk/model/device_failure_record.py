from typing import List

class DiagnosticModule:
    def __init__(self, diagnosticModuleCode, diagnosticModuleName, diagnosticModuleTypeCode, diagnosticModuleTypeName, typeOfDiagnosticModuleType):
        self.diagnosticModuleCode = diagnosticModuleCode
        self.diagnosticModuleName = diagnosticModuleName
        self.diagnosticModuleTypeCode = diagnosticModuleTypeCode
        self.diagnosticModuleTypeName = diagnosticModuleTypeName
        self.typeOfDiagnosticModuleType = typeOfDiagnosticModuleType

    def __repr__(self):
        return f"DiagnosticModule(diagnosticModuleCode={self.diagnosticModuleCode}, diagnosticModuleName={self.diagnosticModuleName}, diagnosticModuleTypeCode={self.diagnosticModuleTypeCode}, diagnosticModuleTypeName={self.diagnosticModuleTypeName}, typeOfDiagnosticModuleType={self.typeOfDiagnosticModuleType})"

class DeviceFailureRecord:
    def __init__(self, alarmGroupCode, alarmGroupName, alarmType, alarmCode, description, alarmNumber, level, status, keywords, earliestAlarmTime, latestAlarmTime, deviceCode, diagnosticModules:List[DiagnosticModule]):
        self.alarmGroupCode = alarmGroupCode
        self.alarmGroupName = alarmGroupName
        self.alarmType = alarmType
        self.alarmCode = alarmCode
        self.description = description
        self.alarmNumber = alarmNumber
        self.level = level
        self.status = status
        self.keywords = keywords
        self.earliestAlarmTime = earliestAlarmTime
        self.latestAlarmTime = latestAlarmTime
        self.deviceCode = deviceCode
        self.diagnosticModules = diagnosticModules

    def __repr__(self):
        return (f"DeviceFailureRecord(alarmGroupCode={self.alarmGroupCode}, "
                f"alarmGroupName={self.alarmGroupName}, "
                f"alarmType={self.alarmType}, "
                f"alarmCode={self.alarmCode}, "
                f"description={self.description}, "
                f"alarmNumber={self.alarmNumber}, "
                f"level={self.level}, "
                f"status={self.status}, "
                f"keywords={self.keywords}, "
                f"earliestAlarmTime={self.earliestAlarmTime}, "
                f"latestAlarmTime={self.latestAlarmTime}, "
                f"deviceCode={self.deviceCode}, "
                f"diagnosticModules={self.diagnosticModules!r})")


    # @staticmethod
    # def from_row(row):
    #     return DeviceFailureRecord(
    #         dfem_code=row['dfem_code'],
    #         display_name=row['display_name'],
    #         dfem_bjlx=row['dfem_bjlx'],
    #         dfem_sxmsbh=row['dfem_sxmsbh'],
    #         description=row['description'],
    #         dfem_bjs=row['dfem_bjs'],
    #         dfem_bjdj=row['dfem_bjdj'],
    #         dfem_zt=row['dfem_zt'],
    #         dfem_gjz=row['dfem_gjz'],
    #         dfem_zzbjsj=row['dfem_zzbjsj'],
    #         dfem_zxbjsj=row['dfem_zxbjsj'],
    #         device_code=row['device_code'],
    #         fm_code=row['fm_code'],
    #         fm_name=row['fm_name']
    #     )


# # 创建示例对象
# record1 = DeviceFailureRecord(
#     "AG0000121409",
#     "12号定子线棒层间温度运行值持续动态超限",
#     "failure",
#     "FM800412",
#     "12号定子线棒层间温度运行值持续动态超限",
#     4,
#     "注意",
#     "已查看",
#     "定子绕组温度，动态预警",
#     "2024-06-30 12:56:48",
#     "2024-06-30 13:59:48",
#     "T0000000002",
#     "QLJ00001",
#     "定子"
# )
#
# # 打印对象
# print(record1)