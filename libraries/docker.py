#https://pypi.org/project/docker/

import os
import subprocess
import time

# importing my libraries
import sys
#C:\app\OneDrive - Atresmedia Corporacion De Medios De Comunicacion SA\dev\code\vs_code
sys.path.append('./python/libraries') 
import string_tools.parse_string as ps

class docker_cls:
    def __init__(self):
        self.docker_path = "C:\\Program Files\\Docker\\Docker\\Docker Desktop.exe"
        self.status = "Down"
        self.check_docker()
    
    def start_docker(self):
        if os.path.exists(self.docker_path):
            print("Iniciando Docker...")
            subprocess.Popen([self.docker_path], shell=True)
            time.sleep(10)
            while not self.check_docker():
                print("Esperando a que Docker inicie...")
                time.sleep(5)
            print("Docker iniciado con éxito.")        
        else:
            print("Docker Desktop no está instalado en la ruta predeterminada.")
    
    def check_docker(self):
        try:
            result = subprocess.run(["docker", "info"], capture_output=True, text=True)
            if result.returncode == 0:
                self.status = "Up"  
                return True
            else:
                self.status = "Down"
                return False
        except FileNotFoundError:
            self.status = "Down"             
            return False
        
    def stop_docker(self):
        print("Deteniendo Docker...")
        subprocess.run(["taskkill", "/F", "/IM", "Docker Desktop.exe"], shell=True)
        print("Docker detenido con éxito.")          
        self.status = "Down"

    def __del__(self):
        return True


class docker_image_cls:
    def pull(self, image_name):
        subprocess.run(["docker", "pull", image_name])
    
    def list(self):
        result = subprocess.run(["docker", "images", "--format", "{{.Repository}} {{.Tag}} {{.ID}} {{.CreatedSince}} {{.Size}}"], capture_output=True, text=True)
        images = []
        for line in result.stdout.strip().split('\n'):
            #repository, tag, image_id, created_size = ps.limit_split(line,3)
            repository, tag, image_id, created_size = line.split(maxsplit=3)
            images.append({
                "repository": repository,
                "tag": tag,
                "image_id": image_id,
                "created+size": created_size
            })
        return images
    
    def exist(self, image_name):
        result = subprocess.run(["docker", "images", "-q", image_name], capture_output=True, text=True)
        return bool(result.stdout.strip())
    
    def delete(self, image_name):
        subprocess.run(["docker", "rmi", "-f", image_name])
    
    def __del__(self):
        return True


class docker_network_cls:
    def create(self, network_name):
        subprocess.run(["docker", "network", "create", network_name])
    
    def list(self):
        result = subprocess.run(["docker", "network", "ls", "--format", "{{.Driver}} {{.Name}} {{.ID}}"], capture_output=True, text=True)
        networks = []
        for line in result.stdout.strip().split('\n'):
            driver, name, network_id = line.split()
            networks.append({
                "driver": driver,
                "name": name,
                "id": network_id
            })
        return networks
        
    def exist(self, network_name):
        result = subprocess.run(["docker", "network", "ls", "-q", "--filter", f"name={network_name}"], capture_output=True, text=True)
        return bool(result.stdout.strip())
    
    def delete(self, network_name):
        subprocess.run(["docker", "network", "rm", network_name])
    
    def connect(self, network_id, container):
        subprocess.run(["docker", "network", "connect", network_id, container])
    
    def disconnect(self, network_id, container):
        subprocess.run(["docker", "network", "disconnect", network_id, container])
    
    def __del__(self):
        return True


class docker_volume_cls:
    def create(self, volume_name):
        subprocess.run(["docker", "volume", "create", volume_name])
    
    def list(self):
        result = subprocess.run(["docker", "volume", "ls", "--format", "{{.Driver}} {{.Name}}"], capture_output=True, text=True)
        volumes = []
        for line in result.stdout.strip().split('\n'):
            driver, name = line.split()
            volumes.append({
                "driver": driver,
                "name": name
            })
        return volumes
    
    def exist(self, volume_name):
        result = subprocess.run(["docker", "volume", "ls", "-q", "--filter", f"name={volume_name}"], capture_output=True, text=True)
        return bool(result.stdout.strip())
    
    def delete(self, network_name):
        subprocess.run(["docker", "volume", "rm", network_name])
    
    def __del__(self):
        return True


class docker_container_cls:
    def create(self, image_name, container_name=None, command=None, args=None):
        cmd = ["docker", "create"]
        if container_name:
            cmd.extend(["--name", container_name])
        cmd.append(image_name)
        if command:
            cmd.append(command)
        if args:
            cmd.extend(args)
        subprocess.run(cmd)
    
    def list(self):
        result = subprocess.run(["docker", "ps", "-a", "--format", "{{.ID}} {{.Image}} {{.Command}} {{.CreatedAt}} {{.Status}} {{.Ports}} {{.Names}}"], capture_output=True, text=True)
        containers = []
        for line in result.stdout.strip().split('\n'):
            container_id, image, rest = line.split(maxsplit=2)
            moreinfo, name = rest.rsplit(maxsplit=1)
            #moreinfo = command, created_at, status, ports         
            containers.append({
                "id": container_id,
                "image": image,
                "name": name,           
                "moreinfo": moreinfo
            })
        return containers
    
    def exist(self, container_name):
        result = subprocess.run(["docker", "ps", "-aq", "--filter", f"name={container_name}"], capture_output=True, text=True)
        return bool(result.stdout.strip())
    
    def delete(self, container_name):
        subprocess.run(["docker", "rm", "-f", container_name])
       
    def run(self, image_name, container_name=None, command=None, args=None):
        cmd = ["docker", "run", "-d"]
        if container_name:
            cmd.extend(["--name", container_name])
        cmd.append(image_name)
        if command:
            cmd.append(command)
        if args:
            cmd.extend(args)
        subprocess.run(cmd)
    
    def start(self, container_name):
        subprocess.run(["docker", "start", container_name])
    
    def stop(self, container_name):
        subprocess.run(["docker", "stop", container_name])
    
    def restart(self, container_name):
        subprocess.run(["docker", "restart", container_name])
    
    def kill(self, container_name):
        subprocess.run(["docker", "kill", container_name])
    
    def status(self, container_name):
        result = subprocess.run(["docker", "inspect", "--format", "{{.State.Status}}", container_name], capture_output=True, text=True)
        return result.stdout.strip()


    def logs(self, container_name):
        result = subprocess.run(["docker", "logs", container_name], capture_output=True, text=True)
        print(result.stdout)
    
    def exec(self, container_name, command):
        subprocess.run(["docker", "exec", container_name] + command.split())
    
    def __del__(self):
        return True


def main():
    objdocker = docker_cls()
    if objdocker.status == "Down":
        objdocker.start_docker()

    objimage = docker_image_cls()
    objnetwork = docker_network_cls()
    objvolume = docker_volume_cls()
    objcontainer = docker_container_cls()

    # objimage.pull("alpine")
    # images = objimage.list()
    # print("Images:", images)
    # image_exists = objimage.exist("alpine")
    # print("Alpine image exists:", image_exists)

    # objvolume.create("alpine_volume")
    # volumes = objvolume.list()
    # print("Volumes:", volumes)
    # volume_exists = objvolume.exist("alpine_volume")
    # print("Alpine volume exists:", volume_exists)

    command = "sh"
    args = ["-c", "while true; do echo 'Hello World'; sleep 1; done"]
    # objcontainer.create("alpine", container_name="alpine_container", command=command, args=args)
    # containers = objcontainer.list()
    # print("Containers:", containers)
    # container_exists = objcontainer.exist("alpine_container")
    # print("Alpine container exists:", container_exists)
    
    # objcontainer.start("alpine_container")
    # objcontainer.restart("alpine_container")    
    # objcontainer.stop("alpine_container")
    # result = objcontainer.status("alpine_container")
    # print(result)
    # objcontainer.start("alpine_container")
    # objcontainer.kill("alpine_container")

    # objcontainer.start("alpine_container")
    # cmd = "ls -l"
    # objcontainer.exec("alpine_container", cmd)

    # objcontainer.delete("alpine_container")
    # objcontainer.run("alpine", container_name="alpine_container", command=command, args=args)
    # objcontainer.logs("alpine_container")
    # objcontainer.stop("alpine_container")


    # objnetwork.create("alpine_network")
    # networks = objnetwork.list()
    # print("Networks:", networks)
    # network_exists = objnetwork.exist("alpine_network")
    # print("Alpine network exists:", network_exists)

    # objnetwork.connect("alpine_network", "alpine_container")
    # objnetwork.disconnect("alpine_network", "alpine_container")

    # objcontainer.delete("alpine_container")
    # objnetwork.delete("alpine_network")
    # objvolume.delete("alpine_volume")
    # objimage.delete("alpine")

    objdocker.stop_docker()

    print("Fin")

if __name__ == "__main__":
    main()
