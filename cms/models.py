from django.db import models

# Create your models here.
from django.utils import timezone


class Organization(models.Model):
    Name = models.CharField(max_length=20, verbose_name="名称")
    Description = models.CharField(max_length=50, verbose_name="描述", null=True, blank=True)
    Status = models.IntegerField(verbose_name="状态", default=0)

    def __str__(self):
        return "{0}".format(self.Name)


class Role(models.Model):
    Name = models.CharField(max_length=20, verbose_name="名称")
    Description = models.CharField(max_length=50, verbose_name="描述", null=True, blank=True)
    Status = models.IntegerField(verbose_name="状态", default=0, blank=True)

    def __str__(self):
        return "{0}".format(self.Name)


class User(models.Model):
    Name = models.CharField(max_length=20, verbose_name="姓名")
    Password = models.CharField(max_length=30, verbose_name="密码")
    Description = models.CharField(max_length=50, verbose_name="描述", null=True, blank=True)
    RealName = models.CharField(max_length=10, verbose_name="真实姓名")
    Status = models.IntegerField(verbose_name="状态", default=0)
    Organization = models.ForeignKey(Organization, verbose_name="组织")
    Role = models.ForeignKey(Role, verbose_name="角色")
    MaxUpload = models.IntegerField(verbose_name="最大上传", default=5)
    MaxDownload = models.IntegerField(verbose_name="最大下载", default=5)

    class Meta:
        index_together = ["Name"]

    def __str__(self):
        return "{0}:{1}".format(self.Name, self.Description)


class CameraGroup(models.Model):
    Name = models.CharField(max_length=20, verbose_name="名称")
    Description = models.CharField(max_length=50, verbose_name="描述", null=True, blank=True)
    Creator = models.ForeignKey(User, verbose_name="创建人")
    CreatedTime = models.DateTimeField(default=timezone.now(), verbose_name="创建时间")

    # Parent = models.ForeignKey(CameraGroup, verbose_name="父节点")

    def __str__(self):
        return "{0}".format(self.Name)


class Camera(models.Model):
    Name = models.CharField(max_length=20, verbose_name="名称")
    DeviceType = models.IntegerField(verbose_name="类型")
    Creator = models.ForeignKey(User, verbose_name="创建人")
    Group = models.ForeignKey(CameraGroup, verbose_name="分组")
    Latitude = models.FloatField(verbose_name="纬度", default=0)
    Longitude = models.FloatField(verbose_name="经度", default=0)

    # Parent = models.ForeignKey(CameraGroup, verbose_name="父节点")

    def __str__(self):
        return "{0}".format(self.Name)


class CameraTree(models.Model):
    Cameras = models.ForeignKey(Camera, verbose_name="摄像头")
    Parent = models.ForeignKey(CameraGroup, verbose_name="父节点")
    # 0：Group ,1: Camera
    ChildType = models.IntegerField(verbose_name="节点类型", default=0)

    def __str__(self):
        return "{0}".format(self.Name)
