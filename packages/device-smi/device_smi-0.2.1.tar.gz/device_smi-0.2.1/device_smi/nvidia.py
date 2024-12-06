import os

from .base import BaseDevice, BaseInfo, BaseMetrics, _run, Pcie, GPU


class NvidiaGPU(BaseInfo):
    def __init__(self, features=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.features = features


class NvidiaGPUMetrics(BaseMetrics):
    pass


class NvidiaDevice(BaseDevice):
    def __init__(self, cls, index: int = 0):
        super().__init__(index)
        self.gpu_id = self._get_gpu_id()

        try:
            args = [
                "nvidia-smi",
                f"--id={self.gpu_id}",
                "--query-gpu="
                "name,"
                "memory.total,"
                "pci.bus_id,"
                "pcie.link.gen.max,"
                "pcie.link.gen.current,"
                "driver_version",
                "--format=csv,noheader,nounits",
            ]

            result = _run(args=args)

            output = result.strip().split("\n")[0]
            model, total_memory, pci_bus_id, pcie_gen, pcie_width, driver = (output.split(", "))

            result = _run(args=["nvidia-smi", "-q", "-i", f"{self.gpu_id}"])
            firmware = " ".join([line.split(":", 1)[1].strip() for line in result.splitlines() if "VBIOS" in line])

            if model.lower().startswith("nvidia"):
                model = model[len("nvidia"):]

            compute_cap = (
                _run(["nvidia-smi", "--format=csv", "--query-gpu=compute_cap", "-i", f"{self.gpu_id}"])
                .removeprefix("compute_cap\n")
            )

            cls.type = "gpu"
            cls.model = model.strip().lower()
            cls.memory_total = int(total_memory) * 1024 * 1024  # bytes
            cls.vendor = "nvidia"
            cls.features = [compute_cap]
            cls.pcie = Pcie(gen=int(pcie_gen), speed=int(pcie_width), id=pci_bus_id)
            cls.gpu = GPU(driver=driver, firmware=firmware)
        except FileNotFoundError:
            raise FileNotFoundError()
        except Exception as e:
            raise e

    def _get_gpu_id(self):
        cudas = os.environ.get("CUDA_VISIBLE_DEVICES", "")
        cuda_list = cudas.split(",") if cudas else []
        if cuda_list and len(cuda_list) > self.index:
            return cuda_list[self.index]
        else:
            return str(self.index)

    def metrics(self):
        try:
            args = ["nvidia-smi", f"--id={self.gpu_id}", "--query-gpu=memory.used,utilization.gpu", "--format=csv,noheader,nounits", ]
            result = _run(args=args)

            output = result.split("\n")[0]
            used_memory, utilization = output.split(", ")

            return NvidiaGPUMetrics(
                memory_used=int(used_memory) * 1024 * 1024,  # bytes
                memory_process=0,  # Bytes, TODO, get this
                utilization=float(utilization),
            )

        except FileNotFoundError:
            raise FileNotFoundError(
                "The 'nvidia-smi' command was not found. Please ensure that the 'nvidia-utils' package is installed."
            )
        except Exception as e:
            raise e
